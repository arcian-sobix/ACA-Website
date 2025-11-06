# ========================================
# ACA Bot Graph Engine
# ========================================
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from uuid import UUID

import discord
from discord import Embed, Interaction, app_commands
from discord.ext import commands
from sqlalchemy import select, and_, func, insert
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from .database import get_db_session
from .encryption import encryption
from .models import User, Node, Edge, Badge, user_badges
from .config import settings

logger = logging.getLogger(__name__)

class ACAGraphEngine:
    """Core graph traversal engine for ACA Bot"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self._cooldowns = {}
    
    async def get_user_state(
        self, 
        user_id: int, 
        guild_id: int, 
        project_slug: str = "arcium"
    ) -> Tuple[User, int]:
        """Fetch user state with caching"""
        cache_key = f"user:{user_id}:guild:{guild_id}:project:{project_slug}:state"
        
        cached = await self.redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            # Reconstruct User from dict
            user = User(**data["user"])
            return user, data["node_id"]
        
        async with get_db_session() as session:
            stmt = select(User).where(
                User.user_id == user_id,
                User.guild_id == guild_id,
                User.project_id == settings.get_project_id(project_slug)
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                user = User(
                    user_id=user_id,
                    guild_id=guild_id,
                    project_id=settings.get_project_id(project_slug),
                    current_node_id=settings.get_root_node_id(project_slug, "explorer"),
                    encrypted_payload=encryption.encrypt_record({"path_history": [], "preferences": {}})
                )
                session.add(user)
                await session.commit()
            
            node_id = user.current_node_id
            
            # Cache for 24h
            await self.redis.setex(
                cache_key,
                timedelta(hours=24),
                json.dumps({"user": user.__dict__, "node_id": node_id})
            )
            
            return user, node_id
    
    async def traverse_edge(
        self,
        user_id: int,
        guild_id: int,
        edge_id: int,
        project_slug: str = "arcium"
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """Attempt edge traversal"""
        async with get_db_session() as session:
            stmt = select(Edge).where(Edge.edge_id == edge_id)
            result = await session.execute(stmt)
            edge = result.scalar_one()
            
            if not edge:
                return False, "Invalid path", None
            
            user, current_node = await self.get_user_state(user_id, guild_id, project_slug)
            
            if current_node != edge.from_node_id:
                return False, "Invalid path", None
            
            # Cooldown check
            cooldown_key = f"cooldown:{user_id}:{edge_id}"
            if await self.redis.exists(cooldown_key):
                return False, "Cooldown active", None
            
            if edge.cooldown_seconds > 0:
                await self.redis.setex(
                    cooldown_key,
                    timedelta(seconds=edge.cooldown_seconds),
                    "1"
                )
            
            if edge.condition_json:
                can_traverse, reason = await self._evaluate_condition(
                    user, edge.condition_json, session
                )
                if not can_traverse:
                    return False, reason, None
            
            # Update user
            user.current_node_id = edge.to_node_id
            user.ec_total += edge.ec_gain
            
            payload = encryption.decrypt_record(user.encrypted_payload)
            payload["path_history"].append({
                "from": edge.from_node_id,
                "to": edge.to_node_id,
                "at": datetime.utcnow().isoformat(),
                "ec_gain": edge.ec_gain
            })
            user.encrypted_payload = encryption.encrypt_record(payload)
            
            # Award badges
            badge_ids = await self._check_badge_eligibility(user, session)
            for badge_id in badge_ids:
                await session.execute(
                    insert(user_badges).values(
                        user_id=user_id,
                        guild_id=guild_id,
                        project_id=user.project_id,
                        badge_id=badge_id
                    )
                )
            
            await session.commit()
            
            # Invalidate cache
            cache_key = f"user:{user_id}:guild:{guild_id}:project:{project_slug}:state"
            await self.redis.delete(cache_key)
            
            return True, None, edge.to_node_id
    
    async def _evaluate_condition(
        self,
        user: User,
        condition: dict,
        session: AsyncSession
    ) -> Tuple[bool, str]:
        """Evaluate condition JSON"""
        op = condition.get("op")
        
        if op == "min_ec":
            if user.ec_total < condition.get("val", 0):
                return False, f"Requires {condition['val']} EC"
        
        elif op == "has_badge":
            slug = condition.get("slug")
            stmt = select(Badge).where(
                Badge.project_id == user.project_id,
                Badge.slug == slug
            )
            result = await session.execute(stmt)
            badge = result.scalar_one_or_none()
            
            if badge:
                badge_check = select(user_badges).where(
                    user_badges.c.user_id == user.user_id,
                    user_badges.c.guild_id == user.guild_id,
                    user_badges.c.badge_id == badge.badge_id
                )
                if not (await session.execute(badge_check)).first():
                    return False, f"Requires '{badge.name}' badge"
        
        return True, ""
    
    async def _check_badge_eligibility(
        self,
        user: User,
        session: AsyncSession
    ) -> List[int]:
        """Check badge eligibility"""
        stmt = select(Badge).where(
            Badge.project_id == user.project_id,
            Badge.required_ec <= user.ec_total
        )
        badges = (await session.execute(stmt)).scalars().all()
        
        earned_ids = []
        for badge in badges:
            earned = select(user_badges).where(
                user_badges.c.user_id == user.user_id,
                user_badges.c.guild_id == user.guild_id,
                user_badges.c.badge_id == badge.badge_id
            )
            if not (await session.execute(earned)).first():
                if badge.required_nodes:
                    payload = encryption.decrypt_record(user.encrypted_payload)
                    completed = {h["to"] for h in payload["path_history"]}
                    if set(badge.required_nodes).issubset(completed):
                        earned_ids.append(badge.badge_id)
                else:
                    earned_ids.append(badge.badge_id)
        
        return earned_ids
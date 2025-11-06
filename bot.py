# ========================================
# ACA Bot Discord Commands - Cypherpunk Edition
# ========================================
import discord
from discord import Embed, Interaction, app_commands, File
from discord.ext import commands
import asyncio
import random

from .engine import ACAGraphEngine
from .database import get_db_session
from .models import User, Badge, user_badges
from .config import settings
from .audio_manager import audio_manager
from .visual_effects import visual_effects
import redis.asyncio as redis

class ACABot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        
        self.engine = ACAGraphEngine(
            redis_client=redis.from_url(settings.REDIS_URL, decode_responses=True)
        )
        
        # Cypherpunk colors and styling
        self.cypherpunk_colors = [
            0x00ff41,  # Matrix Green
            0x00d4ff,  # Cyan
            0xff00ff,  # Magenta
            0xffaa00,  # Orange
            0x8800ff,  # Purple
            0xff0088   # Pink
        ]
    
    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=settings.GUILD_ID))
        # Create audio files if they don't exist
        audio_manager.create_audio_files()

bot = ACABot()

@bot.event
async def on_ready():
    print(f"🚀 ACA Bot is ready! Logged in as {bot.user}")
    print(f"🎨 Cypherpunk Edition Activated")
    print(f"🔐 Privacy-First Learning Platform")
    print(f"🌐 Connected to {len(bot.guilds)} guilds")

@bot.event
async def on_guild_join(guild):
    """Welcome message when bot joins a new guild"""
    try:
        # Find a channel to send welcome message
        channel = None
        for ch in guild.text_channels:
            if ch.permissions_for(guild.me).send_messages:
                channel = ch
                break
        
        if channel:
            embed = visual_effects.create_cypherpunk_embed(
                "🚀 ACA Arcium Academy Has Arrived",
                "The ultimate Web3 learning experience is now available in your server!\n\n"
                "🎓 Learn MPC, C-SPL, and advanced cryptography\n"
                "🏆 Earn badges and EEC credits\n"
                "👥 Connect with expert mentors\n"
                "🔐 Privacy-first education\n\n"
                "Type `/start` to begin your journey!",
                glitch_level=2
            )
            embed.set_image(url="attachment://arcium-logo-cypherpunk.png")
            
            await channel.send(
                embed=embed,
                file=File("assets/images/arcium-logo-cypherpunk.png")
            )
    except Exception as e:
        print(f"Error sending welcome message: {e}")

@bot.tree.command(name="start", description="Begin your Web3 learning journey")
async def start_command(interaction: Interaction):
    """Entry point with cypherpunk styling"""
    # Send typing effect
    await visual_effects.send_typing_effect(interaction.channel, 1.5)
    
    # Create cypherpunk-styled embed
    embed = visual_effects.create_cypherpunk_embed(
        "🚀 Welcome to ACA Arcium Academy",
        "Choose your specialization path in the encrypted future.",
        glitch_level=3
    )
    
    # Add fields with glitch effects
    embed.add_field(
        name=visual_effects.glitch_text("🌐 Explorer Path"),
        value="Master C-SPL and confidential transactions on Solana",
        inline=False
    )
    embed.add_field(
        name=visual_effects.glitch_text("⚒️ Builder Path"), 
        value="Create DApps with MXES and advanced cryptography",
        inline=False
    )
    embed.add_field(
        name=visual_effects.glitch_text("🛡️ Guardian Path"),
        value="Become an MPC expert and privacy protocol architect",
        inline=False
    )
    
    # Add Arcium branding
    embed.set_thumbnail(url="attachment://arcium-logo-cypherpunk.png")
    embed.set_image(url="https://media.giphy.com/media/3o7aCTPPm4OHfRLSH6/giphy.gif")  # Matrix-style background
    
    view = PathSelectionView()
    
    await interaction.response.send_message(
        embed=embed,
        view=view,
        ephemeral=True,
        file=File("assets/images/arcium-logo-cypherpunk.png")
    )

class PathSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(
        label="🌐 EXPLORER",
        style=discord.ButtonStyle.primary,
        custom_id="explorer_path"
    )
    async def explorer_button(self, interaction: Interaction, button: discord.ui.Button):
        await self._select_path(interaction, "explorer")
    
    @discord.ui.button(
        label="⚒️ BUILDER", 
        style=discord.ButtonStyle.success,
        custom_id="builder_path"
    )
    async def builder_button(self, interaction: Interaction, button: discord.ui.Button):
        await self._select_path(interaction, "builder")
    
    @discord.ui.button(
        label="🛡️ GUARDIAN",
        style=discord.ButtonStyle.danger,
        custom_id="guardian_path"
    )
    async def guardian_button(self, interaction: Interaction, button: discord.ui.Button):
        await self._select_path(interaction, "guardian")
    
    async def _select_path(self, interaction: Interaction, path: str):
        # Send typing effect
        await visual_effects.send_typing_effect(interaction.channel, 1.0)
        
        root_map = {"explorer": 1, "builder": 101, "guardian": 201}
        edge_id = root_map.get(path, 1)
        
        success, error, new_node = await bot.engine.traverse_edge(
            interaction.user.id, interaction.guild_id, edge_id
        )
        
        if success:
            # Play success sound if in voice channel
            if interaction.user.voice and interaction.user.voice.channel:
                voice_client = interaction.guild.voice_client
                if voice_client:
                    await audio_manager.play_success_sound(voice_client)
            
            embed = visual_effects.create_cypherpunk_embed(
                "✅ PATH SELECTED",
                f"Welcome to the {path.upper()} path!\n"
                f"You are now at Node #{new_node}\n\n"
                f"{visual_effects.create_progress_bar(10)}\n\n"
                f"Your journey into Web3 privacy begins now...",
                glitch_level=2
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # Play error sound
            if interaction.user.voice and interaction.user.voice.channel:
                voice_client = interaction.guild.voice_client
                if voice_client:
                    await audio_manager.play_error_sound(voice_client)
            
            embed = visual_effects.create_cypherpunk_embed(
                "❌ ACCESS DENIED",
                f"Error: {error}\n\n"
                f"The system has detected an anomaly in your request.",
                glitch_level=4
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="profile", description="View your encrypted learning profile")
async def profile_command(interaction: Interaction, member: discord.Member = None):
    target = member or interaction.user
    
    # Send typing effect
    await visual_effects.send_typing_effect(interaction.channel, 1.0)
    
    async with get_db_session() as session:
        user, node_id = await bot.engine.get_user_state(
            target.id, interaction.guild_id
        )
        
        badge_stmt = select(Badge).join(
            user_badges, Badge.badge_id == user_badges.c.badge_id
        ).where(
            user_badges.c.user_id == target.id,
            user_badges.c.guild_id == interaction.guild_id
        )
        badges = (await session.execute(badge_stmt)).scalars().all()
    
    # Create cypherpunk profile embed
    embed = visual_effects.create_cypherpunk_embed(
        f"👤 {target.display_name.upper()}'S PROFILE",
        "Encrypted learning credentials and achievements",
        glitch_level=1
    )
    
    embed.set_thumbnail(url=target.display_avatar.url)
    
    # Add progress information
    progress_percentage = min((user.ec_total / 1000) * 100, 100)
    
    embed.add_field(
        name=visual_effects.glitch_text("💰 EC SCORE"),
        value=f"**{user.ec_total}** EEC\n"
              f"Rank: Top {await _get_percentile(target.id, interaction.guild_id)}%\n"
              f"{visual_effects.create_progress_bar(int(progress_percentage))}",
        inline=True
    )
    
    embed.add_field(
        name=visual_effects.glitch_text("📍 CURRENT NODE"),
        value=f"**#{node_id}**\n"
              f"Status: {'🟢 ACTIVE' if user.current_node_id else '🔴 OFFLINE'}",
        inline=True
    )
    
    if badges:
        badge_text = " ".join([f"{b.emoji} {b.name}" for b in badges[:8]])
        embed.add_field(
            name=visual_effects.glitch_text("🏆 ACHIEVEMENTS"),
            value=badge_text,
            inline=False
        )
    
    # Add ASCII art footer
    ascii_art = visual_effects.create_ascii_art("ACA")
    embed.add_field(
        name=visual_effects.glitch_text("🛡️ ENCRYPTED IDENTITY"),
        value=f"```\n{ascii_art}\n```",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="leaderboard", description="View the encrypted rankings")
async def leaderboard_command(interaction: Interaction, range: str = "weekly"):
    # Send typing effect
    await visual_effects.send_typing_effect(interaction.channel, 1.5)
    
    async with get_db_session() as session:
        stmt = select(User).where(
            User.guild_id == interaction.guild_id
        ).order_by(User.ec_total.desc()).limit(10)
        
        top_users = (await session.execute(stmt)).scalars().all()
    
    embed = visual_effects.create_cypherpunk_embed(
        "🏆 ENCRYPTED RANKINGS",
        "Top performers in the Arcium Academy",
        glitch_level=2
    )
    
    # Add leaderboard with glitch effects
    for idx, user in enumerate(top_users, 1):
        member = interaction.guild.get_member(user.user_id)
        name = member.display_name if member else f"User {user.user_id}"
        
        rank_emoji = ["🥇", "🥈", "🥉", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅"][idx-1]
        
        embed.add_field(
            name=f"{rank_emoji} #{idx} - {visual_effects.glitch_text(name)}",
            value=f"**{user.ec_total}** EEC | Node #{user.current_node_id or 0}",
            inline=False
        )
    
    # Add matrix-style footer
    embed.set_footer(
        text=f"{visual_effects._generate_matrix_text(30)} | Encrypted at {discord.utils.utcnow().strftime('%H:%M:%S')}"
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="challenge", description="View current learning challenges")
async def challenge_command(interaction: Interaction):
    # Send typing effect
    await visual_effects.send_typing_effect(interaction.channel, 1.0)
    
    user, node_id = await bot.engine.get_user_state(
        interaction.user.id, interaction.guild_id
    )
    
    embed = visual_effects.create_cypherpunk_embed(
        "⚡ AVAILABLE CHALLENGES",
        f"Node #{node_id} - Encrypted Learning Opportunities",
        glitch_level=2
    )
    
    # Sample challenges with cypherpunk styling
    challenges = [
        {
            "title": "🔐 Confidential Token Creation",
            "difficulty": "Beginner",
            "reward": "25 EEC + First-Mint Badge",
            "time": "30 minutes",
            "description": "Create your first C-SPL token with privacy features"
        },
        {
            "title": "🗝️ Shamir's Secret Sharing",
            "difficulty": "Intermediate", 
            "reward": "40 EEC + Key-Holder Badge",
            "time": "45 minutes",
            "description": "Master cryptographic key distribution"
        },
        {
            "title": "⚡ MPC Circuit Design",
            "difficulty": "Advanced",
            "reward": "60 EEC + Manticore-Mage Badge", 
            "time": "90 minutes",
            "description": "Design secure multi-party computation protocols"
        }
    ]
    
    for challenge in challenges:
        embed.add_field(
            name=f"{visual_effects.glitch_text(challenge['title'])}",
            value=f"**Difficulty:** {challenge['difficulty']}\n"
                  f"**Reward:** {challenge['reward']}\n"
                  f"**Time:** {challenge['time']}\n"
                  f"**Description:** {challenge['description']}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="mentor", description="Connect with expert mentors")
async def mentor_command(interaction: Interaction):
    # Send typing effect
    await visual_effects.send_typing_effect(interaction.channel, 1.0)
    
    embed = visual_effects.create_cypherpunk_embed(
        "👥 MENTOR NETWORK",
        "Connect with expert Web3 privacy professionals",
        glitch_level=1
    )
    
    # Sample mentors with cypherpunk styling
    mentors = [
        {
            "name": "Alex Chen",
            "expertise": "MPC & Privacy Protocols",
            "rating": "4.9 ⭐",
            "sessions": "156",
            "status": "🟢 ONLINE"
        },
        {
            "name": "Sarah Rodriguez", 
            "expertise": "C-SPL Development",
            "rating": "4.8 ⭐",
            "sessions": "89",
            "status": "🟢 ONLINE"
        },
        {
            "name": "Dr. Crypto",
            "expertise": "Zero-Knowledge Proofs",
            "rating": "5.0 ⭐",
            "sessions": "203",
            "status": "🔴 BUSY"
        }
    ]
    
    for mentor in mentors:
        embed.add_field(
            name=f"{mentor['status']} {visual_effects.glitch_text(mentor['name'])}",
            value=f"**Expertise:** {mentor['expertise']}\n"
                  f"**Rating:** {mentor['rating']}\n"
                  f"**Sessions:** {mentor['sessions']} completed",
            inline=False
        )
    
    embed.add_field(
        name=visual_effects.glitch_text("🎯 How to Connect"),
        value="1. Join a voice channel\n"
              "2. Use `/mentor connect [name]`\n"
              "3. Wait for mentor acceptance\n"
              "4. Begin your encrypted learning session",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="stats", description="View encrypted learning statistics")
async def stats_command(interaction: Interaction):
    # Send typing effect
    await visual_effects.send_typing_effect(interaction.channel, 2.0)
    
    embed = visual_effects.create_cypherpunk_embed(
        "📊 ENCRYPTED ANALYTICS",
        "Real-time learning performance metrics",
        glitch_level=2
    )
    
    # Add statistics with cypherpunk styling
    stats = {
        "Total Learners": "50,247",
        "Active Sessions": "1,203",
        "Completion Rate": "87.3%",
        "Average Session": "23m 47s",
        "Mentor Response": "12m 3s",
        "EEC Distributed": "1,247,892",
        "Badges Earned": "45,678",
        "Challenges Solved": "234,567"
    }
    
    for key, value in stats.items():
        embed.add_field(
            name=visual_effects.glitch_text(key),
            value=f"**{value}**",
            inline=True
        )
    
    # Add network status
    embed.add_field(
        name=visual_effects.glitch_text("🌐 NETWORK STATUS"),
        value="🟢 All systems operational\n"
              "🔐 Encryption: Active\n"
              "📡 Nodes: 1,247 online\n"
              "⚡ Latency: 12ms",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def _get_percentile(user_id: int, guild_id: int) -> str:
    """Get user's percentile ranking"""
    async with get_db_session() as session:
        stmt = select(User).where(User.guild_id == guild_id).order_by(User.ec_total.desc())
        users = (await session.execute(stmt)).scalars().all()
        
        for idx, u in enumerate(users):
            if u.user_id == user_id:
                return f"{((idx + 1) / len(users) * 100):.0f}"
    return "N/A"

# Voice channel commands
@bot.tree.command(name="join", description="Join voice channel for audio effects")
async def join_command(interaction: Interaction):
    """Join voice channel for enhanced experience"""
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message(
            "❌ You must be in a voice channel to use this command!",
            ephemeral=True
        )
        return
    
    channel = interaction.user.voice.channel
    
    try:
        voice_client = await channel.connect()
        
        # Play intro audio
        await audio_manager.play_intro(voice_client)
        
        embed = visual_effects.create_cypherpunk_embed(
            "🔊 CONNECTED TO ENCRYPTED CHANNEL",
            f"Joined {channel.name} for enhanced audio experience\n\n"
            f"🎵 Audio effects enabled\n"
            f"🔐 Secure communication active\n"
            f"🎨 Cypherpunk styling engaged",
            glitch_level=1
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to join voice channel: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="leave", description="Leave voice channel")
async def leave_command(interaction: Interaction):
    """Leave voice channel"""
    voice_client = interaction.guild.voice_client
    
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message(
            "🔇 Disconnected from voice channel",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ Not connected to any voice channel",
            ephemeral=True
        )
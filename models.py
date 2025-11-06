from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, ForeignKey, Text, JSON, Binary, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), primary_key=True)
    
    current_node_id = Column(Integer)
    ec_total = Column(Integer, default=0)
    badge_cache = Column(JSON)
    mentor_score = Column(Numeric(3, 2), default=1.0)
    is_mentor = Column(Boolean, default=False)
    encrypted_payload = Column(Binary, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    project = relationship("Project", back_populates="users")
    badges = relationship("Badge", secondary="user_badges", back_populates="users")

class Project(Base):
    __tablename__ = 'projects'
    
    project_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_slug = Column(String, unique=True, nullable=False)
    project_name = Column(String, nullable=False)
    encryption_key_id = Column(String, ForeignKey('vault_keys.key_id'), nullable=False)
    config = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    users = relationship("User", back_populates="project")
    nodes = relationship("Node", back_populates="project")
    edges = relationship("Edge", back_populates="project")
    badges = relationship("Badge", back_populates="project")

class Node(Base):
    __tablename__ = 'nodes'
    
    node_id = Column(Integer, primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text)
    content_text = Column(Text)
    media_url = Column(String)
    
    parent_node_id = Column(Integer, ForeignKey('nodes.node_id'))
    required_ec = Column(Integer, default=0)
    required_badges = Column(JSON)
    required_roles = Column(JSON)
    
    is_checkpoint = Column(Boolean, default=False)
    is_root = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    project = relationship("Project", back_populates="nodes")
    parent = relationship("Node", remote_side=[node_id])

class Edge(Base):
    __tablename__ = 'edges'
    
    edge_id = Column(Integer, primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), nullable=False)
    
    from_node_id = Column(Integer, ForeignKey('nodes.node_id'), nullable=False)
    to_node_id = Column(Integer, ForeignKey('nodes.node_id'), nullable=False)
    
    choice_text = Column(String, nullable=False)
    choice_order = Column(Integer, default=0)
    
    condition_json = Column(JSON)
    ec_gain = Column(Integer, default=0)
    cooldown_seconds = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    
    project = relationship("Project", back_populates="edges")

class Badge(Base):
    __tablename__ = 'badges'
    
    badge_id = Column(Integer, primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), nullable=False)
    
    slug = Column(String, nullable=False)
    name = Column(String, nullable=False)
    emoji = Column(String)
    description = Column(Text)
    role_id = Column(BigInteger)
    
    required_nodes = Column(JSON)
    required_ec = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    
    project = relationship("Project", back_populates="badges")
    users = relationship("User", secondary="user_badges", back_populates="badges")

class VaultKey(Base):
    __tablename__ = 'vault_keys'
    
    key_id = Column(String, primary_key=True)
    key_version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    rotated_at = Column(DateTime)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    
    log_id = Column(BigInteger, primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), nullable=False)
    
    user_id = Column(BigInteger)
    guild_id = Column(BigInteger)
    action = Column(String, nullable=False)
    
    payload_hash = Column(String, nullable=False)
    payload = Column(JSON)
    
    created_at = Column(DateTime, server_default=func.now())

class DeletionQueue(Base):
    __tablename__ = 'deletion_queue'
    
    queue_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), nullable=False)
    requested_at = Column(DateTime, server_default=func.now())
    processed_at = Column(DateTime)

# Association table for many-to-many relationship
user_badges = Table(
    'user_badges',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('user_id', BigInteger, nullable=False),
    Column('guild_id', BigInteger, nullable=False),
    Column('project_id', UUID(as_uuid=True), nullable=False),
    Column('badge_id', Integer, ForeignKey('badges.badge_id'), nullable=False),
    Column('earned_at', DateTime, server_default=func.now()),
    ForeignKeyConstraint(['user_id', 'guild_id', 'project_id'], ['users.user_id', 'users.guild_id', 'users.project_id'])
)
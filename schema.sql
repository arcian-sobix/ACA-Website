-- ========================================
-- ACA BOT V0.1 - PRODUCTION SCHEMA
-- PostgreSQL 15 + TimescaleDB
-- ========================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "timescaledb";

-- Master encryption key metadata
CREATE TABLE vault_keys (
    key_id TEXT PRIMARY KEY,
    key_version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    rotated_at TIMESTAMPTZ
);

INSERT INTO vault_keys (key_id, key_version) VALUES ('aca-master-key-v1', 1);

-- Multi-tenant projects
CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_slug TEXT UNIQUE NOT NULL,
    project_name TEXT NOT NULL,
    encryption_key_id TEXT NOT NULL REFERENCES vault_keys(key_id),
    config JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed Arcium core project
INSERT INTO projects (project_slug, project_name, encryption_key_id, config) VALUES 
('arcium', 'ACA Arcium Academy', 'aca-master-key-v1', '{"colors": {"primary": "#e94560"}, "ec_thresholds": {"graduate": 1000}}');

-- Users table
CREATE TABLE users (
    user_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    project_id UUID NOT NULL REFERENCES projects(project_id),
    
    current_node_id INTEGER,
    ec_total INTEGER DEFAULT 0,
    badge_cache JSONB,
    mentor_score DECIMAL(3,2) DEFAULT 1.0,
    is_mentor BOOLEAN DEFAULT FALSE,
    encrypted_payload BYTEA NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    PRIMARY KEY (user_id, guild_id, project_id)
);

CREATE INDEX idx_users_ec ON users (guild_id, ec_total DESC) WHERE is_mentor = FALSE;
CREATE INDEX idx_users_mentor ON users (guild_id, mentor_score DESC) WHERE is_mentor = TRUE;

-- Learning nodes
CREATE TABLE nodes (
    node_id SERIAL PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id),
    
    title TEXT NOT NULL,
    description TEXT,
    content_text TEXT,
    media_url TEXT,
    
    parent_node_id INTEGER REFERENCES nodes(node_id),
    required_ec INTEGER DEFAULT 0,
    required_badges JSONB,
    required_roles JSONB,
    
    is_checkpoint BOOLEAN DEFAULT FALSE,
    is_root BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(project_id, node_id)
);

-- Path edges
CREATE TABLE edges (
    edge_id SERIAL PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id),
    
    from_node_id INTEGER NOT NULL REFERENCES nodes(node_id),
    to_node_id INTEGER NOT NULL REFERENCES nodes(node_id),
    
    choice_text TEXT NOT NULL,
    choice_order INTEGER DEFAULT 0,
    
    condition_json JSONB,
    ec_gain INTEGER DEFAULT 0,
    cooldown_seconds INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(project_id, from_node_id, to_node_id),
    CHECK (from_node_id != to_node_id)
);

-- Badge definitions
CREATE TABLE badges (
    badge_id SERIAL PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id),
    
    slug TEXT NOT NULL,
    name TEXT NOT NULL,
    emoji TEXT,
    description TEXT,
    role_id BIGINT,
    
    required_nodes JSONB,
    required_ec INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(project_id, slug)
);

-- User-badge mapping
CREATE TABLE user_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    project_id UUID NOT NULL,
    badge_id INTEGER NOT NULL REFERENCES badges(badge_id),
    
    earned_at TIMESTAMPTZ DEFAULT NOW(),
    
    FOREIGN KEY (user_id, guild_id, project_id) REFERENCES users(user_id, guild_id, project_id),
    UNIQUE(user_id, guild_id, project_id, badge_id)
);

-- Audit log (append-only, GDPR compliant)
CREATE TABLE audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id),
    
    user_id BIGINT,
    guild_id BIGINT,
    action TEXT NOT NULL,
    
    payload_hash TEXT NOT NULL,
    payload JSONB,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('audit_log', 'created_at', chunk_time_interval => INTERVAL '1 day');

CREATE INDEX idx_audit_user ON audit_log (project_id, user_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_log (project_id, action, created_at DESC);

-- GDPR deletion queue
CREATE TABLE deletion_queue (
    queue_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    project_id UUID NOT NULL,
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    
    FOREIGN KEY (user_id, guild_id, project_id) REFERENCES users(user_id, guild_id, project_id)
);

CREATE INDEX idx_deletion_pending ON deletion_queue (processed_at) WHERE processed_at IS NULL;
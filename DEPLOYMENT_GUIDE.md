# ACA Arcium Academy V0.1 - Deployment Guide

## 🚀 Quick Start

### Step 1: Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Required variables:
# - DISCORD_TOKEN: Your bot token from Discord Developer Portal
# - GUILD_ID: Your Discord server ID
# - MASTER_ENCRYPTION_KEY: Generate with `openssl rand -hex 32`
```

### Step 2: Database Setup
```bash
# Start PostgreSQL and Redis
docker-compose -f infra/docker-compose.yml up -d postgres redis

# Wait for databases to be ready (30 seconds)
sleep 30

# Initialize database schema
docker exec -i aca-arcium-academy-postgres-1 psql -U aca -d acabot < database/schema.sql
```

### Step 3: Install Dependencies
```bash
cd bot
pip install -r requirements.txt
```

### Step 4: Run the Bot
```bash
python main.py
```

## 📋 Pre-Deployment Checklist

### Discord Configuration
- [ ] Create bot application in Discord Developer Portal
- [ ] Generate bot token
- [ ] Invite bot to your server with these permissions:
  - Send Messages
  - Embed Links
  - Read Message History
  - Use Slash Commands
  - Manage Roles (for badge roles)

### Server Requirements
- [ ] Python 3.11+ installed
- [ ] Docker and Docker Compose installed
- [ ] PostgreSQL 15+ (or use Docker)
- [ ] Redis 7+ (or use Docker)
- [ ] 2GB RAM minimum
- [ ] 10GB storage minimum

### Security Setup
- [ ] Generate secure MASTER_ENCRYPTION_KEY
- [ ] Set up GitHub secrets for CI/CD
- [ ] Configure firewall rules (ports 5432, 6379, 80, 443)
- [ ] Set up SSL certificates for production

## 🔧 Configuration Files

### Environment Variables (.env)
```bash
# Required
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here
DATABASE_URL=postgresql://aca:password@localhost:5432/acabot
REDIS_URL=redis://localhost:6379
MASTER_ENCRYPTION_KEY=your_64_char_hex_key_here

# Optional
VAULT_KEY_ID=aca-master-key-v1
```

### Docker Compose (Production)
```yaml
# Use production database credentials
# Enable SSL/TLS
# Set up health checks
# Configure resource limits
```

## 🐛 Troubleshooting

### Bot Won't Start
```bash
# Check Discord token
echo $DISCORD_TOKEN

# Test database connection
psql $DATABASE_URL -c "SELECT 1;"

# Check Redis connection
redis-cli -u $REDIS_URL ping
```

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker logs aca-arcium-academy-postgres-1

# Reset database (WARNING: Deletes all data)
docker-compose down
docker volume prune
docker-compose up -d
```

### Permission Errors
```bash
# Fix file permissions
chmod +x bot/main.py
sudo chown -R $USER:$USER .
```

## 📊 Monitoring & Logs

### View Bot Logs
```bash
# Direct output
python bot/main.py

# Or use systemd/journalctl (production)
journalctl -u aca-bot -f
```

### Database Monitoring
```bash
# Connect to database
docker exec -it aca-arcium-academy-postgres-1 psql -U aca -d acabot

# Check user count
SELECT COUNT(*) FROM users;

# Check active nodes
SELECT COUNT(*) FROM nodes WHERE project_id = '00000000-0000-0000-0000-000000000001';
```

### Performance Monitoring
```bash
# Redis memory usage
docker exec -it aca-arcium-academy-redis-1 redis-cli info memory

# PostgreSQL performance
docker exec -it aca-arcium-academy-postgres-1 psql -U aca -d acabot -c "SELECT * FROM pg_stat_activity;"
```

## 🔄 CI/CD Deployment

### GitHub Actions Setup
1. Fork this repository
2. Add secrets to GitHub:
   - `DISCORD_TOKEN`
   - `GUILD_ID`
   - `MASTER_ENCRYPTION_KEY`
   - `SERVER_HOST`
   - `SERVER_USER`
   - `SSH_PRIVATE_KEY`

3. Push to `main` branch for auto-deployment

### Manual Deployment
```bash
# Build Docker image
docker build -t aca-bot:latest -f infra/Dockerfile .

# Run with Docker Compose
docker-compose -f infra/docker-compose.yml up -d

# Check deployment
docker-compose ps
docker logs aca-bot
```

## 🛡️ Security Best Practices

### Production Checklist
- [ ] Use strong MASTER_ENCRYPTION_KEY
- [ ] Enable PostgreSQL SSL
- [ ] Configure Redis password
- [ ] Set up firewall rules
- [ ] Enable fail2ban
- [ ] Regular security updates
- [ ] Backup encryption keys
- [ ] Monitor access logs

### GDPR Compliance
- [ ] Implement `/forget` command
- [ ] Set up audit logging
- [ ] Configure data retention policies
- [ ] Document privacy policy
- [ ] Enable user data export

## 📈 Scaling Considerations

### Database Optimization
```sql
-- Add indexes for better performance
CREATE INDEX CONCURRENTLY idx_users_ec_guild ON users(guild_id, ec_total);
CREATE INDEX CONCURRENTLY idx_nodes_project ON nodes(project_id, node_id);
```

### Redis Optimization
```bash
# Increase memory limit
redis-cli config set maxmemory 2gb
redis-cli config set maxmemory-policy allkeys-lru
```

### Bot Sharding (High Traffic)
```python
# Enable sharding in bot configuration
# shard_id = int(os.getenv("SHARD_ID", "0"))
# shard_count = int(os.getenv("SHARD_COUNT", "1"))
```

## 🆘 Support & Resources

### Documentation
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Community
- [Arcium Discord](https://discord.gg/arcium)
- [Discord.py Support Server](https://discord.gg/dpy)

### Emergency Contacts
- Security Issues: security@arcium.com
- Bot Issues: bot-support@arcium.com
- Infrastructure: infra@arcium.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the Arcium Ecosystem** | gMPC ☂️
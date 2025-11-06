# ACA Arcium Academy V0.1

The ultimate interactive Web3 education assistant for the Arcium ecosystem.

## 🚀 Quick Start

```bash
# 1. Clone and checkout branch
git clone https://github.com/arcian-sobix/aca-arcium-academy.git 
cd aca-arcium-academy
git checkout -b v0.1-launch

# 2. Configure environment
cp .env.example .env
# Edit .env with your tokens and keys

# 3. Start infrastructure
docker-compose -f infra/docker-compose.yml up -d

# 4. Run bot
cd bot
pip install -r requirements.txt
python main.py
```

## 📁 Project Structure

- `bot/` - Discord bot code (discord.py 2.3)
- `database/` - PostgreSQL schema and migrations
- `assets/` - Visual diagrams (SVG), demo media
- `docs/` - Pitch materials, security checklists, ROI calculators
- `infra/` - Docker & CI/CD configurations

## 🔐 Environment Variables

```bash
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here
DATABASE_URL=postgresql://aca:password@localhost:5432/acabot
REDIS_URL=redis://localhost:6379
MASTER_ENCRYPTION_KEY=generate_with: openssl rand -hex 32
VAULT_KEY_ID=aca-master-key-v1
```

## 📊 Database Setup

```bash
# Run migrations
psql -d acabot -f database/schema.sql

# Verify installation
psql -d acabot -c "SELECT * FROM projects;"
```

## 🎯 Core Features

- **Graph-based learning**: Non-linear node traversal with conditions
- **Privacy-first**: AES-256 per-record encryption
- **Zero-token rewards**: EEC credits, badge system
- **Sub-project forks**: `/fork` command for instant tenant isolation
- **Analytics**: ClickHouse materialized views for retention tracking

## 📈 Monitoring

Access Grafana at `http://localhost:3000` (admin/admin)
- Node drop-off rates
- User retention (Day 7, Day 30)
- EC distribution histograms

## 🔒 Security

See `docs/SECURITY_CHECKLIST.md` for full audit requirements.

## 📢 Commands

- `/start` - Begin learning journey
- `/profile [@user]` - View progress
- `/leaderboard` - Top 10 learners
- `/challenge` - Current node options

## 📸 Visual Assets

All diagrams are in `assets/diagrams/` as SVG. To convert to PNG:

```bash
# Install rsvg-convert
brew install librsvg  # macOS
sudo apt-get install librsvg2-bin  # Linux

# Convert
rsvg-convert assets/diagrams/ecosystem-architecture.svg -o assets/images/ecosystem.png
```

## 📅 Roadmap

| Milestone | Date | Status |
|-----------|------|--------|
| Schema Review | T+3d | ⏳ Pending |
| MVP Launch | T+42d | 🚧 In Progress |
| V0.2 Analytics | T+70d | 📋 Planned |

## 🤝 Contributing

1. Fork this repository
2. Create feature branch (`git checkout -b feature/new-node`)
3. Add nodes via CSV import
4. Submit PR to `v0.1-launch` branch

## 📄 License

MIT License - See LICENSE file for details.

---

**Built with ❤️ for the Arcium Ecosystem** | gMPC ☂️
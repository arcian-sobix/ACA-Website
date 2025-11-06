# ACA Bot Security & Privacy Checklist

## Encryption & Key Management
- [ ] All PII encrypted at rest (AES-256-GCM, per-record key envelope)
- [ ] Redis cache holds NO PII - only user_id:guild_id → node_id mappings
- [ ] Bot token & encryption keys live in Vault (never committed)
- [ ] Key rotation enabled (90-day cycle)

## Access Control
- [ ] Rate limiting: 10 commands / 60s per user (Redis-Cell)
- [ ] Attachment scanning: ClamAV API for screenshots ≤ 5MB
- [ ] Role-based node access (condition_json validation)
- [ ] Admin commands require role verification

## Compliance
- [ ] GDPR delete: `/forget` - purges encrypted row & audit logs within 24h
- [ ] Audit log: every `/answer` + `/fork` written to append-only log (SHA-256 chain)
- [ ] Data residency: EU users stored in EU region
- [ ] Privacy policy: published at https://arcium.academy/privacy

## Infrastructure Security
- [ ] Network policies: block inter-fork DB access
- [ ] WAF: Cloudflare in front of all bot endpoints
- [ ] DDoS protection: Rate limiting at gateway
- [ ] Secret scanning: GitHub Actions enabled

## Monitoring (Grafana Alerts)
- [ ] Drop-off >30% at any node → Slack #edu-alerts
- [ ] Average EC <20 after 48h → tag @mentor
- [ ] Failed login attempts >5/hr → security team
- [ ] Encryption failure >1/day → P1 incident

## Penetration Testing (Post-MVP)
- [ ] SQL injection testing (SQLAlchemy ORM is safe but verify)
- [ ] Redis key enumeration (ensure no PII in keys)
- [ ] Discord role escalation (test permission boundaries)
- [ ] Fork isolation breach (attempt cross-project data access)
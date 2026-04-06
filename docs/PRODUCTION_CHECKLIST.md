# Guild AI — Production Deployment Checklist

## GCP Resources Required

### Cloud SQL (PostgreSQL)
- [ ] Instance: `guild-db` (PostgreSQL 15, `db-f1-micro` for beta, scale up later)
- [ ] Database: `guild`
- [ ] User: `guild_app` with strong password
- [ ] Enable private IP for Cloud Run VPC connector

### Memorystore (Redis)
- [ ] Instance: `guild-redis` (Standard tier, 1GB)
- [ ] Same VPC as Cloud Run

### Secret Manager
- [ ] `guild-database-url` — `postgresql+asyncpg://guild_app:PASSWORD@PRIVATE_IP:5432/guild`
- [ ] `guild-redis-url` — `redis://REDIS_IP:6379/0`
- [ ] `guild-secret-key` — random 64-char string
- [ ] `guild-paystack-secret` — Paystack secret key
- [ ] `guild-firebase-sa` — Firebase service account JSON (optional, for Admin SDK)

### Vertex AI
- [ ] Enable `aiplatform.googleapis.com` API
- [ ] Enable `generativelanguage.googleapis.com` API
- [ ] Ensure the Cloud Run service account has `roles/aiplatform.user`

### Firebase
- [ ] Project: `guild-ai-080`
- [ ] Enable Authentication (Email/Password + Google provider)
- [ ] Add production domain to authorized domains

### Cloud Build
- [ ] Connect GitHub repo as trigger source
- [ ] Trigger: on push to `main` branch
- [ ] Service account needs: Cloud Run Admin, Secret Manager Accessor, Cloud SQL Client

### Cloud Run
- [ ] Service: `guild-api`
- [ ] Region: `us-central1`
- [ ] CPU: 1, Memory: 1GB
- [ ] Min instances: 0, Max: 10
- [ ] Concurrency: 80
- [ ] VPC connector for Cloud SQL + Redis access

### Custom Domain
- [ ] Map `api.tryguild.ai` → Cloud Run service
- [ ] Map `app.tryguild.ai` → Cloud Run service (or CDN)
- [ ] SSL certificates auto-managed by Cloud Run

## Pre-Deployment Steps
1. Run `alembic upgrade head` against Cloud SQL
2. Verify Firebase auth works with production domain
3. Test Paystack webhooks with production keys
4. Set `ALLOWED_ORIGINS` to `["https://tryguild.ai", "https://app.tryguild.ai"]`
5. Set `APP_ENV=production` and `DEBUG=False`

## Post-Deployment Verification
1. `curl https://api.tryguild.ai/health` → `{"status": "ok"}`
2. Test signup flow end-to-end
3. Test content generation then approval
4. Verify WebSocket connects at `wss://api.tryguild.ai/ws/{user_id}`
5. Verify Celery Beat tasks execute on schedule

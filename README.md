# Guild AI

**AI-powered content-to-customer growth engine for solopreneurs and small businesses.**

Guild learns your business through conversation, then runs the complete flywheel: create content → publish on schedule → capture engaged leads → nurture to conversion → learn what works → repeat.

## Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Vertex AI (Gemini 2.0 Flash/Pro), Anthropic Claude (fallback) |
| **Media** | Imagen 3 (images), Veo 3 (video) |
| **Backend** | FastAPI, SQLAlchemy (async), Celery + Redis |
| **Database** | PostgreSQL 15 |
| **Vector DB** | Qdrant (RAG pipeline) |
| **Auth** | Firebase Authentication |
| **Billing** | Paystack (3-tier subscription) |
| **Frontend** | React 19, Vite, Tailwind CSS v4 |
| **Infrastructure** | Docker Compose, Google Cloud Run |

## Architecture

```
Frontend (React + Vite)
    ↕ REST + WebSocket
API Layer (FastAPI — 56+ endpoints)
    ├── Auth (Firebase JWT)
    ├── Content Pipeline (Generate → Judge → Approve → Publish)
    ├── CRM (Lead Capture → Score → Nurture → Convert)
    ├── Calendar (Smart scheduling + external sync)
    ├── Goals (Track → Milestone → Repeat with escalation)
    ├── Workflows (11 templates, AI builder, custom DAGs)
    └── 27 Agents (via Agent Registry + Orchestrator)
        ↕
    Services Layer
    ├── LLM Client (Vertex AI primary, Claude fallback, circuit breaker)
    ├── Token Tracker (per-call cost, budget alerts)
    ├── Judge Agent (rubric + evaluator league)
    ├── RAG Pipeline (Qdrant + Vertex AI embeddings)
    └── 30 Integration Connectors
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 22+
- Python 3.11+

### Local Development

```bash
# 1. Clone and configure
git clone https://github.com/ArnovZ080/Guild-AI-New.git
cd Guild-AI-New
cp .env.example .env  # Edit with your keys

# 2. Start infrastructure
docker compose up -d db redis qdrant

# 3. Run database migrations
pip install -r requirements.txt
alembic upgrade head

# 4. Start the API server
uvicorn services.api.main:app --reload --port 8001

# 5. Start the frontend (separate terminal)
cd services/web
npm install
npm run dev
```

### Production Build

```bash
# Build and run everything (frontend + backend in one image)
docker compose -f docker-compose.prod.yml up --build
```

## API Overview

| Group | Prefix | Endpoints |
|---|---|---|
| Auth | `/api/auth` | register, verify, me |
| Onboarding | `/api/onboarding` | status, chat, complete |
| Content | `/api/content` | generate, queue, approve, reject, edit, publish, performance |
| CRM | `/api/crm` | contacts CRUD, pipeline, lead scoring, engagement capture |
| Calendar | `/api/calendar` | events, daily-brief, sync, suggest-time |
| Goals | `/api/goals` | CRUD, progress, milestones, repeat |
| Dashboard | `/api/dashboard` | snapshot |
| Subscription | `/api/subscription` | plans, create, webhook, usage |
| Integrations | `/api/integrations` | connectors, connect, disconnect |
| WebSocket | `/ws/{user_id}` | Real-time agent events |
| Health | `/health` | DB + Redis connectivity check |

## Frontend Views

| Route | View | Purpose |
|---|---|---|
| `/` | Chat | Claude-style conversational interface |
| `/content` | Content Queue | 3-tab: Queue, Calendar, Published |
| `/theater` | Agent Theater | Real-time agent activity monitoring |
| `/growth` | Growth Dashboard | Stats, insights, goals, leads |
| `/workflows` | Workflow Builder | Templates, AI builder, custom DAGs |
| `/settings` | Settings | Profile, integrations, billing, knowledge base |

## Environment Variables

See [`.env.example`](.env.example) for all required variables.

## Deployment

See [`docs/PRODUCTION_CHECKLIST.md`](docs/PRODUCTION_CHECKLIST.md) for the complete GCP deployment guide.

## License

Proprietary — © 2026 Guild AI. All rights reserved.

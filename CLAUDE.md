# CLAUDE.md — Guild-AI-New

## Project Overview

Guild-AI is a **Small Business Executive Suite** — a multi-agent AI platform that helps small businesses automate marketing, sales, customer intelligence, finance, and operations workflows. It uses a sophisticated agent orchestration system where a central Orchestrator delegates tasks to specialized agents, runs them through a quality evaluation pipeline, and streams real-time activity to a React dashboard.

---

## Tech Stack

### Backend
| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn |
| Language | Python 3.11 |
| LLM | OpenAI (primary), Vertex AI / Gemini Flash (fallback) |
| Database | PostgreSQL via SQLAlchemy 2.0 + Alembic migrations |
| Task queue | Celery with Redis broker |
| Caching / Event bus | Redis |
| Vector DB | Qdrant |
| Config | Pydantic Settings (`pydantic-settings`) |

### Frontend
| Layer | Technology |
|---|---|
| Framework | React 19 + Vite 7 |
| Routing | React Router DOM 7 |
| Styling | Tailwind CSS 4 + `tailwind-merge` + `class-variance-authority` |
| Animations | Framer Motion 12 |
| UI primitives | Radix UI (`@radix-ui/react-slot`, `@radix-ui/react-tooltip`) |
| Icons | Lucide React |
| Workflow visualization | ReactFlow |
| Toasts | React Toastify |

### Infrastructure
- **Docker**: Multi-stage build (Node 20 for frontend build, Python 3.11 slim for runtime)
- **CI/CD**: Google Cloud Build (`cloudbuild.yaml`) → Container Registry → Cloud Run (`us-central1`)

---

## Directory Structure

```
Guild-AI-New/
├── services/
│   ├── api/                      # FastAPI REST API (port 8001)
│   │   ├── main.py               # App factory, middleware, router registration
│   │   └── routes/
│   │       ├── agents.py         # Agent list/run + event streaming
│   │       ├── identity.py       # Business identity management
│   │       ├── integrations.py   # Integration status/config
│   │       ├── oauth.py          # OAuth callback flows
│   │       ├── subscription.py   # Subscription management
│   │       └── waitlist.py       # Waitlist sign-ups
│   │
│   ├── core/                     # Business logic "Brain"
│   │   ├── config.py             # Settings via pydantic-settings (reads .env)
│   │   ├── llm.py                # LLMClient with circuit-breaker + Vertex fallback
│   │   ├── logging.py            # Structured logger
│   │   ├── worker.py             # Celery worker definition
│   │   ├── bridge.py             # Legacy bridge adapter
│   │   │
│   │   ├── agents/               # Core agent framework
│   │   │   ├── base.py           # BaseAgent ABC + AgentConfig
│   │   │   ├── registry.py       # AgentRegistry (global singleton dict)
│   │   │   ├── models.py         # Pydantic models: DelegationSpec, TaskResult, AgentEvent, etc.
│   │   │   ├── orchestrator.py   # OrchestratorAgent — main planning & execution loop
│   │   │   ├── evaluator.py      # EvaluatorLeague (FactChecker, BrandCompliance, SEO)
│   │   │   ├── content.py        # ContentAgent
│   │   │   ├── research.py       # ResearchAgent
│   │   │   ├── identity.py       # Business identity manager
│   │   │   ├── authorization.py  # Human-in-the-loop auth queue
│   │   │   ├── projects.py       # Project & milestone manager
│   │   │   ├── secrets.py        # Secrets management
│   │   │   ├── subscription_models.py
│   │   │   └── triggers.py       # Event-based task triggers
│   │   │
│   │   ├── adk/                  # Autonomous Development Kit — pre-built agents
│   │   │   ├── business_intelligence.py   # BusinessIntelligenceAgent
│   │   │   ├── customer_intelligence.py   # CustomerIntelligenceAgent
│   │   │   ├── financial_advisor.py       # FinancialAdvisorAgent
│   │   │   ├── marketing_strategist.py    # MarketingStrategistAgent
│   │   │   ├── trend_analyst.py           # TrendAnalystAgent
│   │   │   ├── marketing/        # Marketing sub-agents
│   │   │   ├── sales/            # Sales sub-agents
│   │   │   ├── hr/               # HR sub-agents
│   │   │   └── operations/       # Operations sub-agents
│   │   │
│   │   ├── workflows/            # Pre-built workflow templates
│   │   │   ├── templates.py      # register_all_templates() — all named workflows
│   │   │   ├── executor.py       # WorkflowExecutor
│   │   │   ├── models.py         # WorkflowTemplate, WorkflowStep, RiskLevel
│   │   │   └── agent_bus.py      # Workflow-level event integration
│   │   │
│   │   ├── integrations/         # External service connectors
│   │   │   ├── registry.py       # register_all_connectors()
│   │   │   ├── oauth.py          # OAuth flow helpers
│   │   │   ├── hubspot.py        # HubSpot CRM
│   │   │   ├── salesforce.py     # Salesforce CRM
│   │   │   ├── google.py         # Google integrations
│   │   │   ├── social.py         # Social media
│   │   │   ├── seo.py            # SEO tools
│   │   │   ├── paystack.py       # Paystack payments
│   │   │   ├── *_bridge.py       # Bridge wrappers for agent use
│   │   │   └── connectors/       # Thin connector implementations
│   │   │       ├── stripe.py, sendgrid.py, twitter.py, hubspot.py, etc.
│   │   │       └── legacy/       # Migrated legacy connector implementations
│   │   │
│   │   ├── customers/            # Customer intelligence models
│   │   │   ├── models.py         # Customer data models
│   │   │   ├── journey_tracker.py
│   │   │   └── predictive_engine.py  # Churn prediction, proactive tasks
│   │   │
│   │   ├── learning/             # Adaptive learning system
│   │   │   ├── adaptive_service.py   # Provides context to Orchestrator
│   │   │   ├── outcome_tracker.py    # Records task outcomes for learning
│   │   │   ├── preference_learner.py
│   │   │   └── models.py
│   │   │
│   │   ├── security/             # Security subsystem
│   │   │   ├── security_middleware.py  # SecurityMiddleware + SecurityHeadersMiddleware
│   │   │   ├── rate_limiter.py         # IP-based rate limiting (1000 req/hr default)
│   │   │   ├── input_sanitizer.py      # Prompt injection detection
│   │   │   ├── pii_detector.py         # PII scrubbing in logs
│   │   │   ├── secure_logger.py        # PII-aware audit logger
│   │   │   ├── auth_service.py         # Authentication helpers
│   │   │   └── env_validator.py        # Startup env variable validation
│   │   │
│   │   ├── db/base.py            # SQLAlchemy base / session setup
│   │   ├── interfaces/voice.py   # Voice interface agent
│   │   ├── tools/document_processor.py
│   │   └── utils/
│   │       ├── event_bus.py      # Singleton EventBus (Redis + in-memory buffer)
│   │       └── logging_utils.py
│   │
│   ├── mcp/                      # Model Context Protocol service (port 8000)
│   │   ├── main.py               # FastAPI app for MCP tool exposure
│   │   ├── router_base.py
│   │   └── routes/
│   │       ├── ads.py, crm.py, seo.py
│   │
│   └── web/                      # React/Vite frontend
│       ├── src/
│       │   ├── App.jsx           # Router, layout, sidebar, public vs. app routes
│       │   ├── main.jsx          # React entry point
│       │   ├── pages/            # Route-level page components
│       │   ├── components/       # Feature components
│       │   │   ├── chat/         # Executive Chat (ChatInterface.jsx)
│       │   │   ├── theater/      # Agent Activity Theater (real-time event stream)
│       │   │   ├── transparency/ # Agent Activity Feed
│       │   │   ├── workflows/    # Workflow Builder (ReactFlow canvas)
│       │   │   ├── connectors/   # Integration connector management
│       │   │   └── ui/           # Shared primitives (button, card, badge, input)
│       │   ├── services/
│       │   │   ├── api.js              # Axios/fetch wrapper for backend API
│       │   │   └── AgentActivityService.js  # Polls /agents/events for Theater
│       │   └── lib/utils.js      # cn() Tailwind class merger
│       ├── vite.config.js
│       ├── tailwind.config.js
│       └── package.json
│
├── data/
│   ├── business_identity.json    # Persisted business identity (name, niche, brand voice)
│   └── secrets.json              # Runtime secrets store (gitignored in prod)
│
├── scripts/                      # Verification & utility scripts
│   ├── verify_*.py               # Phase/feature verification scripts
│   └── import_legacy_integrations.py
│
├── verify_*.py                   # Root-level verification scripts (older phases)
├── requirements.txt              # Python dependencies
├── Makefile                      # Developer commands
├── Dockerfile                    # Multi-stage production build
└── cloudbuild.yaml               # Google Cloud Build CI/CD pipeline
```

---

## Core Architecture Patterns

### Agent Pattern
All agents extend `BaseAgent` (`services/core/agents/base.py`):

```python
class MyAgent(BaseAgent):
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        # Core logic here
        return result
```

- `run()` is the public interface (called by orchestrator). It wraps `process()` with event emission, error handling, and `TaskResult` packaging.
- `process()` is where agent-specific logic lives. Must be async.
- Agents self-register with `AgentRegistry` at module import time:
  ```python
  AgentRegistry.register(AgentCapability(
      name="MyAgent",
      category="CategoryName",
      capabilities=["capability1"],
      description="...",
      agent_class=MyAgent
  ))
  ```

### Orchestration Flow
1. Client sends a goal to `OrchestratorAgent.process()`
2. Orchestrator fetches business identity context, adaptive learning context, and proactive customer intelligence
3. LLM generates a `DelegationPlan` — a DAG of `DelegationSpec` tasks
4. Orchestrator executes tasks respecting dependency order and budget constraints
5. Each task result passes through `EvaluatorLeague` (FactChecker + BrandCompliance + [SEO]) — threshold 0.8
6. Failed evaluations trigger retries up to `task.retry_limit`
7. Tasks with `authority_level = "human"` are queued for human approval via `auth_queue`
8. All state changes emit events to `EventBus` for the Agent Theater UI

### EventBus
`services/core/utils/event_bus.py` — thread-safe singleton:
- **Emit**: `event_bus.emit(AgentEvent(...))`
- **Read**: `event_bus.get_events(since_id, limit)` — Redis-backed with in-memory fallback
- The frontend polls `GET /agents/events?since_id=<id>&limit=50` for real-time updates

### LLM Client
`services/core/llm.py` — circuit breaker pattern:
- **Primary**: OpenAI GPT-4 Turbo Preview
- **Fallback**: Vertex AI / Gemini Flash (triggered after 3 consecutive failures)
- Circuit breaker resets after 60 seconds
- Default instance: `from services.core.llm import default_llm`

### Workflow Templates
Registered in `services/core/workflows/templates.py` via `register_all_templates()`. Available workflows:
- `customer_onboarding` — Welcome sequence with profile enrichment
- `customer_retention` — At-risk customer detection and outreach
- `content_campaign` — Research → Create → Evaluate → Publish
- `lead_nurture` — Qualify → Enrich → Pitch → Outreach
- `financial_review` — Monthly financial aggregation and reporting
- `competitive_intel` — Competitor research and strategy update
- `grand_opening` — Full business launch sequence (master workflow)

---

## Configuration

Settings are in `services/core/config.py` via `pydantic-settings`. All values can be overridden via environment variables or a `.env` file in the project root.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:password@localhost:5432/guild` | PostgreSQL connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis for EventBus |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery broker |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/2` | Celery results |
| `OPENAI_API_KEY` | `None` | Required for LLM features |
| `QDRANT_URL` | `http://localhost:6333` | Vector database |
| `SECRET_KEY` | `changeme` | **Must be changed in production** |
| `ALLOWED_ORIGINS` | `["http://localhost:3000"]` | CORS origins |
| `APP_ENV` | `local` | Environment name |
| `DEBUG` | `False` | Debug mode |

**Create a `.env` file at the project root** — it is gitignored and loaded automatically.

---

## Development Commands

```bash
# Backend setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run API server (port 8001)
make run-api
# or directly:
uvicorn services.api.main:app --reload

# Run MCP service (port 8000)
uvicorn services.mcp.main:app --host 0.0.0.0 --port 8000

# Run tests
make test
# or directly:
pytest services/core services/api

# Lint and format
make lint
# Equivalent to:
black services
flake8 services
mypy services

# Frontend development
cd services/web
npm install
npm run dev      # Dev server (port 5173)
npm run build    # Production build
npm run lint     # ESLint
npm run preview  # Preview production build locally

# Docker build
docker build -t guild-ai-new .

# Deploy (via Cloud Build)
# Push to connected branch — cloudbuild.yaml triggers automatically
```

---

## API Endpoints

### API Service (`services/api/main.py`, port 8001)

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/agents/` | List all registered agents |
| `POST` | `/agents/{name}/run` | Run a specific agent |
| `GET` | `/agents/events` | Poll agent activity events (Theater) |
| `GET/POST` | `/identity/*` | Business identity CRUD |
| `GET/POST` | `/integrations/*` | Integration management |
| `GET/POST` | `/oauth/*` | OAuth callback handling |
| `GET/POST` | `/waitlist/*` | Waitlist management |
| `GET/POST` | `/subscription/*` | Subscription management |

### MCP Service (`services/mcp/main.py`, port 8000)

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/mcp/tools` | List available MCP tools |
| various | `/mcp/ads/*` | Ad platform tools |
| various | `/mcp/crm/*` | CRM tools |
| various | `/mcp/seo/*` | SEO tools |

---

## Security

The security subsystem (`services/core/security/`) applies across all API requests:

- **SecurityHeadersMiddleware**: Adds `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, `Referrer-Policy`, `Content-Security-Policy` to all responses.
- **SecurityMiddleware**: Rate limiting (1000 req/hr per IP), prompt injection detection on POST/PUT/PATCH bodies, PII-aware audit logging.
- **PII Detector**: Scrubs sensitive data from logs before writing.
- **Environment Validator**: Checks for exposed secrets on startup.
- **Input Sanitizer**: Detects and blocks high-severity prompt injection attempts (HTTP 400).
- **CORS**: Configured in `services/api/main.py` — set `ALLOWED_ORIGINS` properly in production (currently `*`).

---

## Frontend Routes

### Public Pages (no sidebar)
- `/landing` — Marketing landing page
- `/login` — Login
- `/signup` — Sign-up
- `/waitlist` — Waitlist
- `/pricing` — Pricing
- `/privacy`, `/terms`, `/refund` — Legal pages

### App Pages (sidebar shown)
- `/` — Executive Dashboard
- `/chat` — Executive Chat (direct agent interaction)
- `/calendar` — Strategic Calendar
- `/content` — Content Hub
- `/workflows` — Workflow Builder (ReactFlow canvas)
- `/memory` — Memory Agent
- `/connectors` — Integration Connector Manager
- `/onboarding` — Onboarding Flow
- `/settings` — (stub, coming soon)

---

## Adding a New Agent

1. Create a file in `services/core/agents/` or `services/core/adk/`.
2. Extend `BaseAgent` and implement `process()`.
3. At module level, call `AgentRegistry.register(AgentCapability(..., agent_class=YourAgent))`.
4. Import the module in `services/api/routes/agents.py` (triggers registration).
5. The agent is now available via `POST /agents/{YourAgentName}/run` and usable by the Orchestrator.

## Adding a New Workflow Template

In `services/core/workflows/templates.py`, inside `register_all_templates()`:

```python
WorkflowExecutor.register_template(
    WorkflowTemplate(
        name="my_workflow",
        display_name="My Workflow",
        description="...",
        category="category_name",
    )
    .add_step("Step Name", "AgentName", "method_name",
               params={"key": "{template_var}"},
               risk_level=RiskLevel.LOW,
               dependencies=["Previous Step Name"])
)
```

## Adding a New API Route

1. Create a file in `services/api/routes/`.
2. Define a `router = APIRouter(prefix="/path", tags=["tag"])`.
3. Import and register in `services/api/main.py` via `app.include_router(your_module.router)`.

---

## Testing

- Test runner: `pytest`
- Test directories: `services/core/` and `services/api/`
- Existing tests: `services/core/tests/test_security.py`
- Verification scripts: `scripts/verify_*.py` and root-level `verify_*.py` — used to verify specific phases of implementation
- Run all: `make test` or `pytest services/core services/api`

### Code Quality
- **Formatter**: `black services` (PEP 8, 88-char line length)
- **Linter**: `flake8 services`
- **Type checker**: `mypy services`
- Run all: `make lint`

---

## Key Conventions

1. **All agent logic is async** — use `async def process(...)` and `await` all LLM calls.
2. **LLM JSON parsing**: Always strip markdown fences before `json.loads()`:
   ```python
   clean = response.replace("```json", "").replace("```", "").strip()
   data = json.loads(clean)
   ```
3. **Event emission**: Emit `AgentEvent` objects via `event_bus.emit(...)` at key steps (THINKING, HANDOFF, COMPLETED, FAILED) to populate the Theater UI.
4. **Registry pattern**: Never instantiate agents directly in routes — use `AgentRegistry.get(name)` and then `capability.agent_class(config)`.
5. **Pydantic everywhere**: All data models use Pydantic v2. Use `model_dump()` / `model_dump_json()` (not `.dict()` / `.json()`).
6. **Config is a singleton**: Import `from services.core.config import settings` — never instantiate `Settings()` again.
7. **No hardcoded credentials**: All secrets via env vars / `.env` file. The `SECRET_KEY` default `"changeme"` must be overridden in production.
8. **Frontend `cn()` helper**: Always use `cn()` from `src/lib/utils.js` for conditional Tailwind classes (wraps `clsx` + `tailwind-merge`).
9. **Component organization**: UI primitives in `src/components/ui/`, feature components in named subdirectories.

---

## Deployment

### Production Deployment (Google Cloud Run)
The `cloudbuild.yaml` automates:
1. Docker multi-stage build (frontend compiled, then embedded in Python container)
2. Push to `gcr.io/$PROJECT_ID/guild-ai-new`
3. Deploy to Cloud Run in `us-central1`, port 8080

The production entrypoint is:
```
uvicorn services.api.main:app --host 0.0.0.0 --port 8080
```

### Environment Variables for Production
Must set in Cloud Run environment:
- `OPENAI_API_KEY`
- `DATABASE_URL` (Cloud SQL)
- `REDIS_URL` (Memorystore)
- `SECRET_KEY` (strong random value)
- `ALLOWED_ORIGINS` (your frontend domain)
- `APP_ENV=production`

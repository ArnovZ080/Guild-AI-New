"""
Guild-AI API Server — Phase 2

FastAPI application with all flywheel routes mounted.
"""
import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from services.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="AI-powered content-to-customer growth engine",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
    return response


# ── Mount all routes ──
from services.api.routes import auth, onboarding, subscription, content, crm, calendar, goals, ws

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])
app.include_router(content.router, prefix="/api/content", tags=["Content Pipeline"])
app.include_router(crm.router, prefix="/api/crm", tags=["CRM"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
app.include_router(ws.router, tags=["WebSocket"])


# ── Health check ──
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME, "version": "2.0.0"}

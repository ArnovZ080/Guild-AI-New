"""
Guild-AI API Server

FastAPI application entry point.
Route structure follows GUILD_AI_MASTER_INSTRUCTIONS_v2.md Section 4.
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


# Process time middleware
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
    return response


# ── Mount route modules ──
from services.api.routes import auth, onboarding, subscription

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])


# ── Health check ──
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME, "version": "2.0.0"}

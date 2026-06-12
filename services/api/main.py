"""
Guild-AI API Server — Production

FastAPI application with all routes, security hardening, and production middleware.
"""
import time
import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="AI-powered content-to-customer growth engine",
)

from services.core.config import settings as _settings
if _settings.APP_ENV == "production" and _settings.SECRET_KEY == "changeme":
    raise RuntimeError(
        "SECRET_KEY is still 'changeme' in production. "
        "Set a real SECRET_KEY env var before deploying."
    )

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Security headers ──
@app.middleware("http")
async def security_headers(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# ── Global exception handler ──
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
        },
    )


# ── Mount all routes ──
from services.api.routes import (
    auth, onboarding, subscription, content, crm, calendar, goals, ws, dashboard, waitlist,
    media, admin, agents, identity, integrations, oauth, chat
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])
app.include_router(content.router, prefix="/api/content", tags=["Content Pipeline"])
app.include_router(crm.router, prefix="/api/crm", tags=["CRM"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(waitlist.router, prefix="/api", tags=["Waitlist"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(media.router)
app.include_router(agents.router, prefix="/api/v1")
app.include_router(identity.router, prefix="/api/v1")
app.include_router(integrations.router, prefix="/api/v1")
app.include_router(oauth.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

app.include_router(ws.router, tags=["WebSocket"])

# ── Force register all connectors ──
from services.core.integrations.registry import register_all_connectors
register_all_connectors()

# ── Serve uploaded media files ──
import os
from fastapi.staticfiles import StaticFiles

_uploads = settings.MEDIA_UPLOAD_DIR
if os.path.isdir(_uploads):
    app.mount("/media", StaticFiles(directory=_uploads), name="media")

# ── Static files (production: serves frontend build) ──
from fastapi.responses import FileResponse
_dist = os.path.join(os.path.dirname(__file__), "..", "web", "dist")
if os.path.isdir(_dist):
    # Mount assets folder for performance if it exists
    assets_dir = os.path.join(_dist, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Prevent accessing files outside of _dist
        file_path = os.path.abspath(os.path.join(_dist, full_path))
        if not file_path.startswith(os.path.abspath(_dist)):
            return FileResponse(os.path.join(_dist, "index.html"))
            
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(_dist, "index.html"))


# ── Health check (enhanced) ──
@app.get("/health")
async def health_check():
    checks = {"api": "ok"}
    # DB
    try:
        from services.core.db.base import get_db
        from sqlalchemy import text
        async for db in get_db():
            await db.execute(text("SELECT 1"))
            checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {e}"
    # Redis
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.aclose()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e}"

    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "service": settings.APP_NAME, "version": "2.0.0", "checks": checks}

from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Guild AI"
    APP_ENV: str = "local"
    DEBUG: bool = False

    # GCP / Vertex AI
    GCP_PROJECT_ID: str = "guild-ai-080"
    GCP_LOCATION: str = "us-central1"
    GEMINI_FLASH_MODEL: str = "gemini-2.5-flash"
    GEMINI_PRO_MODEL: str = "gemini-2.5-pro"

    # Media generation models (env-overridable — model IDs expire, see docs/superpowers/plans/2026-09-model-migration-note.md)
    IMAGE_MODEL: str = "gemini-2.5-flash-image"
    VIDEO_MODEL: str = "veo-3.1-generate-001"
    VIDEO_MODEL_FAST: str = "veo-3.1-fast-generate-001"

    # Anthropic (fallback only)
    ANTHROPIC_API_KEY: Optional[str] = None

    # Database — Supabase / Neon / Cloud SQL
    # Supabase: postgresql+asyncpg://postgres:pass@db.xxx.supabase.co:5432/postgres
    # Neon:     postgresql+asyncpg://user:pass@ep-xxx.region.neon.tech/guild?sslmode=require
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/guild"

    # Redis — Upstash (free tier) or local
    # Upstash: rediss://default:xxx@xxx.upstash.io:6379
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery — shares Redis (Upstash single DB is fine, Celery uses key prefixes)
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Qdrant — Qdrant Cloud (free tier) or local
    # Cloud: https://xxx.cloud.qdrant.io:6333
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None  # Required for Qdrant Cloud

    # Supabase (Storage + optional DB)
    SUPABASE_URL: str = "https://jypdcueqaoaxuqojwhnn.supabase.co"
    SUPABASE_SERVICE_KEY: Optional[str] = None  # service_role key for server-side storage
    SUPABASE_STORAGE_BUCKET: str = "media"

    # Firebase
    FIREBASE_PROJECT_ID: str = "guild-ai-080"

    # Paystack
    PAYSTACK_SECRET_KEY: Optional[str] = None
    PAYSTACK_PUBLIC_KEY: Optional[str] = None

    # Email sending (Guild-owned SendGrid)
    SENDGRID_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "hello@mail.guildof1.com"
    EMAIL_FROM_NAME: str = "Guild AI"

    # Meta (Facebook + Instagram)
    META_APP_ID: Optional[str] = None
    META_APP_SECRET: Optional[str] = None
    META_REDIRECT_URI: str = "http://localhost:8001/api/v1/oauth/callback/meta"
    APP_ENV: str = "local"  # local | production

    # Security
    SECRET_KEY: str = "changeme"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Media Storage
    MEDIA_UPLOAD_DIR: str = "./uploads/media"
    STORAGE_BACKEND: str = "local"  # "local" or "supabase"
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/webp", "image/gif",
    ]
    ALLOWED_VIDEO_TYPES: List[str] = [
        "video/mp4", "video/quicktime", "video/webm",
    ]

    model_config = {"env_file": ".env", "case_sensitive": True, "extra": "ignore"}


settings = Settings()

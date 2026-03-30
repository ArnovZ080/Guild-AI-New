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
    GEMINI_FLASH_MODEL: str = "gemini-2.0-flash-001"
    GEMINI_PRO_MODEL: str = "gemini-2.0-pro-001"

    # Anthropic (fallback only)
    ANTHROPIC_API_KEY: Optional[str] = None

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/guild"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"

    # Firebase
    FIREBASE_PROJECT_ID: str = "guild-ai-080"

    # Paystack
    PAYSTACK_SECRET_KEY: Optional[str] = None
    PAYSTACK_PUBLIC_KEY: Optional[str] = None

    # Security
    SECRET_KEY: str = "changeme"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()

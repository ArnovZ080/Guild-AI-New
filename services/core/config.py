from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "Guild AI"
    APP_ENV: str = "local"
    DEBUG: bool = False

    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/guild"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    # Qdrant Configuration
    QDRANT_URL: str = "http://localhost:6333"

    # Security
    SECRET_KEY: str = "changeme"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

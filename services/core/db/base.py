from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from services.core.config import settings

# Ensure it uses the asyncpg driver
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Build connection args — Neon, Supabase, and cloud providers require SSL
connect_args = {}
if any(host in db_url for host in ["neon.tech", "supabase.co", "supabase.com"]):
    connect_args["ssl"] = True

engine = create_async_engine(
    db_url,
    echo=False,
    connect_args=connect_args,
    # Cloud DBs autosuspend — pool_pre_ping handles reconnection gracefully
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


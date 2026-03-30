"""
Shared test fixtures for the Guild AI test suite.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from services.core.db.base import Base


# ── Async event loop ──
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ── In-memory SQLite for fast test isolation ──
@pytest.fixture
async def db_session():
    """Provides a clean async DB session backed by in-memory SQLite."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# ── Mock LLM client ──
@pytest.fixture
def mock_llm():
    """Returns a mock LLM client that returns deterministic JSON."""
    client = MagicMock()
    client.chat_completion = AsyncMock(
        return_value='{"result": "mock_response", "status": "success"}'
    )
    return client


# ── Test user helper ──
@pytest.fixture
async def test_user(db_session):
    """Creates a test user in the in-memory DB."""
    from services.core.db.models import UserAccount
    from services.core.security.jwt import get_password_hash

    user = UserAccount(
        email="test@guild.ai",
        hashed_password=get_password_hash("testpass123"),
        tier="free",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

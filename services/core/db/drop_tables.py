import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/guild_ai")

async def drop_tables():
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        tables = ['agent_authorizations', 'ai_action_outcomes', 'learned_patterns', 'agent_triggers']
        for table in tables:
            await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
            print(f"Dropped {table}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(drop_tables())

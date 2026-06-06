import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from services.core.config import settings

async def main():
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        try:
            # Check user_accounts columns
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='user_accounts'"))
            cols = [row[0] for row in result]
            print(f"user_accounts columns: {cols}")
            
            # Check business_identities columns
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='business_identities'"))
            cols = [row[0] for row in result]
            print(f"business_identities columns: {cols}")
            
        except Exception as e:
            print(f"Error: {e}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())

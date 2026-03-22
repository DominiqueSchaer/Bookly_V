import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.settings import settings

async def main():
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT typname FROM pg_type WHERE typname='booking_status'"))
        rows = result.all()
        print('Type rows:', rows)
    await engine.dispose()

asyncio.run(main())

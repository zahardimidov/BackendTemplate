from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import ENGINE, TIMEZONE
from app.infra.database.models import Base

engine = create_async_engine(url=ENGINE, echo=False)
async_session = async_sessionmaker(engine)


async def run_database():
    async with engine.begin() as conn:
        if TIMEZONE and "asyncpg" in ENGINE:
            offset = f'{datetime.now(TIMEZONE).utcoffset().total_seconds() / 3600:+.0f}'
            await conn.execute(text(f"SET TIME ZONE 'UTC{offset}';"))
        await conn.run_sync(Base.metadata.create_all)

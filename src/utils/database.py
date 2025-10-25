from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings

engine = create_async_engine(settings.DB_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

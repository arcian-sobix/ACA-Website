from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .config import settings
from .models import Base

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=20,
    max_overflow=30
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
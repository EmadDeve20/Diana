from datetime import datetime

from contextlib import asynccontextmanager

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.pool import NullPool

from diana.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    poolclass=NullPool,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_db() -> AsyncSession:

    session = AsyncSessionLocal()
    AsyncSession
    try:
        yield session
    finally:
        await session.close()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True, default=None)


async def create_all_tables():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


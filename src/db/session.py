from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import create_engine

import src.config as config
from src.models import Base


engine = create_async_engine(
    config.DATABASE_URL if config.DEBUG else config.DATABASE_URL_PROD,
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class LazyDbInit:
    """
    Create the db schema, just once.
    """
    is_initizalized = False

    @classmethod
    def initialize(cls):
        if not cls.is_initizalized:
            engine = create_engine(f'postgresql://'
                                         f'{config.DB_USER}:'
                                         f'{config.DB_PASS}@'
                                         f'{config.DB_HOST if config.DEBUG else "db"}:'
                                         f'{config.DB_PORT}/'
                                         f'{config.DB_NAME}')

            Base.metadata.create_all(bind=engine)
            cls.is_initizalized = True


async def get_db() -> Generator:
    """Dependency for getting async session"""
    LazyDbInit.initialize()
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()

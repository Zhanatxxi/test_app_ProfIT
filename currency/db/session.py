from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine,
    async_scoped_session
)
from sqlalchemy.orm import sessionmaker


from currency.settings.settings import settings


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=False,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
)

Session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    ),
    scopefunc=current_task
)

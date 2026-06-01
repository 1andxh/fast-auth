import pytest
import os
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings

test_engine = create_async_engine(settings.TEST_DB_URL, echo=False)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)

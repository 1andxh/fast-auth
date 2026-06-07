import pytest
import pytest_asyncio
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from src import app
from src.core.config import settings
from src.db import Base
from src.users.services import UserService

test_engine = create_async_engine(settings.TEST_DB_URL, echo=False, poolclass=NullPool)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope="session", autouse=True)
def apply_mirgations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")
    yield


@pytest_asyncio.fixture(loop_scope="function")
async def db_session():
    async with TestSessionLocal() as session:
        yield session
        await session.commit()

@pytest_asyncio.fixture(autouse=True)
async def clean_database():
    yield

    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )


@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def auth_service():
    from src.auth.services import AuthService
    from src.auth.security import Security

    security = Security()
    user_service = UserService()

    return AuthService(user_service,security)

@pytest.fixture
def session_service(db_session):
    from src.auth.services import SessionService

    return SessionService(db_session)

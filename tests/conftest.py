import pytest
import pytest_asyncio
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src import app
from src.core.config import settings
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
        await session.rollback()


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

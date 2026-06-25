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
from src.auth.security import Security, security
from src.auth.services import SessionService
from datetime import datetime, timezone, timedelta
from src.auth.models import UserSession, RefreshToken
from src.users import User
import uuid
import secrets

from httpx import AsyncClient, ASGITransport
from src.db.session import get_session



test_engine = create_async_engine(settings.TEST_DB_URL, echo=False, poolclass=NullPool)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)

API_PREFIX = "api/v1/auth"


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

@pytest_asyncio.fixture()
async def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def user_service(db_session):
    return UserService(db_session)

@pytest.fixture
def auth_service(db_session):
    from src.auth.services import AuthService

    security = Security()
    user_service = UserService(db_session)

    return AuthService( db_session, user_service,security)

@pytest.fixture
def session_service(db_session):

    return SessionService(db_session)


@pytest.fixture
def refresh_service(db_session):
    from src.auth.services import RefreshTokenService
    from src.auth.security import Security


    security = Security()
    session_service = SessionService(db_session)

    return RefreshTokenService(db_session, session_service, security)


@pytest.fixture
def token_service(db_session, session_service, refresh_service):
    from src.auth.services import TokenService
    from src.auth.security import Security

    security = Security()

    return TokenService(db_session, session_service, refresh_service, security)


@pytest.fixture
def create_test_session(db_session):
    async def _factory(user=None, **kwargs):
        if user is None:
            user = User(
                id=uuid.uuid4(),
                email=f"test@email.com",
                hashed_password="hashed_string"
            )
            db_session.add(user)
            await db_session.flush()

        session_data = {
            "user_id": user.id,
            "user_agent": "Mozilla/5.0",
            "ip_address": "127.0.0.1",
            "expires_at": datetime.now(timezone.utc) + timedelta(days=7)
        }
        session_data.update(kwargs)

        usersession = UserSession(**session_data)
        db_session.add(usersession)
        await db_session.flush()

        return usersession, user
    
    return _factory

@pytest.fixture
def create_test_refresh_token(db_session, create_test_session):
    async def _factory(user_session=None, **kwargs):
        if not user_session:
            user_session, _ = await create_test_session()
        
        raw_token = secrets.token_urlsafe(32)
        hashed_token = security.hash_refresh_token(raw_token)

        token_data = {
            "session_id": user_session.id,
            "token_hash": hashed_token,
            "family_id": uuid.uuid4(),
            "expires_at": datetime.now(timezone.utc) + timedelta(days=30),
            "revoked_at": None
        }
        token_data.update(kwargs)

        token = RefreshToken(**token_data)
        db_session.add(token)
        await db_session.flush()

        return token, raw_token

    return _factory

@pytest.fixture
def create_test_user(db_session):
    async def _factory(email: str = "testing@email.com", password: str = "hashed_pass"):
        hashed = security.hash_password(password=password)
        user = User(email=email, hashed_password=hashed, is_active=True)

        db_session.add(user)
        await db_session.flush()

        return user, password
    
    return _factory



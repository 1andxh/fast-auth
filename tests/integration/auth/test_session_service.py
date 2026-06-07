import pytest
import asyncio
from src.core.exceptions import SessionExpiredError, SessionRevokedError
import uuid
from src.users import User
from src.auth.models import UserSession
from datetime import timedelta, timezone, datetime

async def _create_test_session(db_session, user=None, **kwargs) -> tuple[UserSession, User]:
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

    session = UserSession(**session_data)
    db_session.add(session)
    await db_session.flush()

    return session, user


@pytest.mark.asyncio
async def test_create_session_succes(db_session,session_service):
    test_user = User(id=uuid.uuid4(), email="test@email.com", hashed_password="some-hash", is_active=True)
    db_session.add(test_user)
    await db_session.flush()

    session = await session_service.create_session(user_id=test_user.id, user_agent="mozilla/5.0", ip_address="127.0.0.1")

    assert session.id is not None
    assert session.user_id == test_user.id
    assert session.revoked_at is None

@pytest.mark.asyncio
async def test_get_session_by_id(db_session, session_service):
    session, _ = await _create_test_session(db_session)

    found_session = await session_service.get_session_by_id(session.id)
    assert found_session is not None
    assert found_session.id == session.id


@pytest.mark.asyncio
async def test_revoke_session(db_session, session_service):
    session, _ = await _create_test_session(db_session)
    assert session.revoked_at is None

    await session_service.revoke_session(session)

    assert session.revoked_at is not None



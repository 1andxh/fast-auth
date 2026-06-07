import pytest
import asyncio
from src.core.exceptions import SessionExpiredError, SessionRevokedError
import uuid
from src.users import User
from src.auth.models import UserSession

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
    session = UserSession(user_id=uuid.uuid4(), user_agent="mozilla/5.0", ip_address='127.0.01')
    db_session.add(session)
    await db_session.commit()

    found_session = session_service.get_session_by_id(session.id)
    assert found_session is not None
    assert found_session.id == session.id



import pytest
import asyncio
from src.core.exceptions import SessionExpiredError, SessionRevokedError
import uuid
from src.users import User

@pytest.mark.asyncio
async def test_create_session_succes(db_session,session_service):
    test_user = User(id=uuid.uuid4(), email="test@email.com", hashed_password="some-hash", is_active=True)
    db_session.add(test_user)
    await db_session.flush()

    session = await session_service.create_session(user_id=test_user.id, user_agent="mozilla/5.0", ip_address="127.0.0.1")

    assert session.id is not None
    assert session.user_id == test_user.id
    assert session.revoked_at is None


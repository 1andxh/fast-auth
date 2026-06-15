import pytest
import asyncio
from src.core.exceptions import SessionExpiredError, SessionRevokedError
import uuid
from src.users import User
from src.auth.models import UserSession
from datetime import timedelta, timezone, datetime


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
async def test_get_session_by_id( session_service, create_test_session):
    session, _ = await create_test_session() 

    found_session = await session_service.get_session_by_id(session.id)
    assert found_session is not None
    assert found_session.id == session.id


@pytest.mark.asyncio
async def test_revoke_session( session_service, create_test_session):
    session, _ = await create_test_session()
    assert session.revoked_at is None

    await session_service.revoke_session(session.id)
    assert session.revoked_at is not None

    # with pytest.raises(SessionRevokedError):
    #     await session_service.revoke_session(session)

@pytest.mark.asyncio
async def test_validate_session_raises_if_expired(session_service, create_test_session):
    past_time =  datetime.now(timezone.utc) - timedelta(days=1)

    session, _ = await create_test_session(expires_at=past_time)

    with pytest.raises(SessionExpiredError):
        await session_service.validate_session(session)


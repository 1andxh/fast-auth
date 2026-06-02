import pytest
import asyncio


from src.users.services import UserService
from src.core.exceptions import DuplicateEmailError


@pytest.mark.asyncio
async def test_create_user_success(db_session, user_service):
    user = await user_service.create_user(
        db_session, email="john@doe.com", password_hash="hashed-password"
    )
    assert user.id is not None
    assert user.email == "john@doe.com"
    assert user.hashed_password == "hashed-password"
    assert user.is_active is True
    assert user.is_verified is False


@pytest.mark.asyncio
async def test_create_user_duplicate_email(db_session, user_service):
    await user_service.create_user(
        db_session, email="john@doe.com", password_hash="hash"
    )

    with pytest.raises(DuplicateEmailError):
        await user_service.create_user(
            db_session, email="JOHN@doe.com", password_hash="amother-hash"
        )

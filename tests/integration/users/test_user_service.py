import asyncio
import pytest

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


@pytest.mark.asyncio
async def test_get_user_by_email_normalizes_email(db_session, user_service):
    created_user = await user_service.create_user(
        db_session, email="john@doe.com", password_hash="hash"
    )

    found_user = await user_service.get_by_email(db_session, email="JoHN@DOE.com")

    assert found_user is not None
    assert found_user.email == created_user.email


@pytest.mark.asyncio
async def test_get_user_by_id(db_session, user_service):
    from src.users import User

    dummy_user = User(email="mike@example.com", hashed_password="hash")
    db_session.add(dummy_user)
    await db_session.commit()

    found_user = await user_service.get_by_id(db_session, id=dummy_user.id)

    assert found_user is not None
    assert found_user.id == dummy_user.id

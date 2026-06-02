import pytest


from src.users.services import UserService


@pytest.mark.asyncio
async def test_create_user_success(db_session, user_service: UserService):
    user = await user_service.create_user(
        db_session, email="john@doe.com", password_hash="hashed-password"
    )
    assert user.id is not None
    assert user.email == "john@doe.com"
    assert user.hashed_password == "hashed-password"
    assert user.is_active is True
    assert user.is_verified is False

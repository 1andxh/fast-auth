import pytest
import asyncio
from src.core.exceptions import DuplicateEmailError, InactiveUserError, InvalidCredentialsError

@pytest.mark.asyncio
async def test_register_user(db_session, auth_service):
    user = await auth_service.register(db_session, email="john@doe.com", password="pass")

    assert user.email == "john@doe.com"
    assert user.hashed_password != "pass"



@pytest.mark.asyncio
async def test_duplicate_registration(db_session, auth_service):
    first_registration = await auth_service.register(db_session, email="john@doe.com", password="passpass")

    assert first_registration.email == "john@doe.com"

    with pytest.raises(DuplicateEmailError):
        await auth_service.register(db_session, email="john@doe.com", password="passpass")

@pytest.mark.asyncio
async def test_authentication_success(db_session, auth_service):
    await auth_service.register(db_session, email="john@doe.com", password="pass")
    user =  await auth_service.authenticate(db_session, email="john@doe.com", password="pass")

    assert user is not None
    assert user.email == "john@doe.com"
    

@pytest.mark.asyncio
async def test_authenticate_wrong_password(db_session, auth_service):
    await auth_service.register(db_session, email="john@doe.com", password="pass")
    with pytest.raises(InvalidCredentialsError):
        await auth_service.authenticate(db_session, email="john@doe.com", password="wrongpassword")


@pytest.mark.asyncio
async def test_authenticate_unknown_user(db_session, auth_service):
    with pytest.raises(InvalidCredentialsError):
        await auth_service.authenticate(db_session, email="john@doe.com", password="passpass")


@pytest.mark.asyncio
async def test_authenticate_inactive_user(db_session, auth_service):
    user = await auth_service.authenticate(db_session, email="john@doe.com", password="passpass")

    user.is_active = False
    await db_session.commit()

    with pytest.raises(InactiveUserError):
        await auth_service.authenticate(db_session, email="john@doe.com", password="passpass")

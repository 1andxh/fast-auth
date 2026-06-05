import pytest
import asyncio
from src.core.exceptions import DuplicateEmailError

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


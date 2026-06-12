import pytest
from sqlalchemy import select
from src.auth.utils import validate_access_token

@pytest.mark.asyncio
async def test_create_token_pair_success(token_service, create_test_user):
    user = await create_test_user()

    result =  await token_service.create_token_pair(user=user)

    assert result.access_token is not None
    assert result.refresh_token is not None

    payload = validate_access_token(result.access_token)

    assert payload.sub == user.id
    assert payload.sid is not None
import pytest
from sqlalchemy import select
from src.auth.models import RefreshToken

@pytest.mark.asyncio
async def test_create_token_pair_success(token_service, create_test_user):
    user = await create_test_user()

    result =  await token_service.create_token_pair(user=user)

    assert result.access_token is not None
    assert result.refresh_token is not None

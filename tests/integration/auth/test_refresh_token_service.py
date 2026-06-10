import pytest
import  asyncio
from datetime import datetime, timezone, timedelta
from src.core.exceptions.token import RefreshTokenNotFoundError

import uuid
from src.users import User
from src.auth.models import RefreshToken


@pytest.mark.asyncio
async def test_create_refresh_token_succes(refresh_service, create_test_session):
    user_session,_ =  await create_test_session()

    result =  await refresh_service.create_refresh_token(session_id=user_session.id)

    assert result.raw_token is not None
    assert len(result.raw_token) > 20
    assert result.refresh_token.session_id == user_session.id
    assert result.refresh_token.expires_at is not None

@pytest.mark.asyncio
async def test_get_refresh_token_success(refresh_service, create_test_refresh_token):
    token, _ = await create_test_refresh_token()

    result = await refresh_service.get_refresh_token(token.id)

    assert result is not None
    assert result.id == token.id
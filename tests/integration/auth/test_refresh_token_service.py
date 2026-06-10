import pytest
import  asyncio
from datetime import datetime, timezone, timedelta
from src.core.exceptions.token import RefreshTokenNotFoundError

import uuid
from src.users import User
from src.auth.models import RefreshToken


@pytest.mark.asyncio
async def test_create_refresh_token_succes(db_session, refresh_service, create_test_session):
    user_session,_ =  await create_test_session()

    result =  await refresh_service.create_refresh_token(session_id=user_session.id)

    assert result.raw_token is not None
    assert len(result.raw_token) > 20
    assert result.refresh_token.session_id == user_session.id
    assert result.refresh_token.expires_at is not None

# @pytest.mark.asyncio
# async def test_refresh_token_sets_parents():...

# @pytest.mark.asyncio
# async def test_revoke_refresh_token_success():...

# @pytest.mark.asyncio
# async def test_rotate_refresh_token_success():...

# @pytest.mark.asyncio
# async def test_rotate_token_raises_if_not_found(db_session, refresh_service):
#     # when a non-existent token is found
#     with pytest.raises(RefreshTokenNotFoundError):
#         await refresh_service.rotate_refresh_token(raw_token="token-does-not-exist")


# @pytest.main.asyncio
# async def test_rotate_token_raises_if_expired(db_session, refresh_service):
#     past_time = ...
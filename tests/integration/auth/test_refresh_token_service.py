import pytest
import  asyncio
from datetime import datetime, timezone, timedelta
from src.core.exceptions.token import RefreshTokenNotFoundError

@pytest.mark.asyncio
async def test_refresh_token_succes(db_session):
    pass

@pytest.mark.asyncio
async def test_rotate_refresh_token_sets_parents():...


@pytest.mark.asyncio
async def test_rotate_refresh_token_preserves_family_id():...


@pytest.mark.asyncio
async def test_rotate_token_raises_if_not_found(db_session, refresh_service):
    # when a non-existent token is found
    with pytest.raises(RefreshTokenNotFoundError):
        await refresh_service.rotate_refresh_token(raw_token="token-does-not-exist")



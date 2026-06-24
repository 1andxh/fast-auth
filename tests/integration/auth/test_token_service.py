import pytest
from sqlalchemy import select
from src.auth.utils import validate_access_token

@pytest.mark.asyncio
async def test_create_token_pair_success(token_service, create_test_user):
    user = await create_test_user()

    result =  await token_service.issue_token_pair(user=user)

    assert result.access_token is not None
    assert result.refresh_token is not None

    payload = validate_access_token(result.access_token)

    assert payload.sub == user.id
    assert payload.sid is not None


@pytest.mark.asyncio
async def test_refresh_access_tokens(token_service, create_test_user):
    user = await create_test_user()

    tokens = await token_service.issue_token_pair(user=user)

    refreshed = await token_service.refresh_tokens(tokens.refresh_token)

    assert refreshed.access_token is not None
    assert refreshed.refresh_token is not None

    assert refreshed.refresh_token != tokens.refresh_token
    assert refreshed.access_token != tokens.access_token

@pytest.mark.asyncio
async def test_logout_success(token_service, create_test_user, db_session):
    user = await create_test_user()

    tokens = await token_service.issue_token_pair(user=user)

    await token_service.logout(tokens.refresh_token)
    db_session.expire_all()


    stored_token =  await token_service.refresh_token_service.get_token_by_hash(tokens.refresh_token)
    if not stored_token:
        return

    session =  await token_service.session_service.get_session_by_id(stored_token.session_id)

    assert stored_token.is_revoked is True
    assert session.revoked_at is not None
    

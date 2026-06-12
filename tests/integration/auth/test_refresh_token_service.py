import pytest
from datetime import datetime, timezone, timedelta
from src.core.exceptions.token import RefreshTokenAlreadyRevokedError


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

@pytest.mark.asyncio
async def test_revoke_refresh_token(refresh_service, create_test_refresh_token):
    token, _ = await create_test_refresh_token()

    await refresh_service.revoke_refresh_token(token.id)

    assert token.revoked_at is not None
    assert token.is_revoked is True

@pytest.mark.asyncio
async def test_revoke_refresh_token_raises_if_already_revoked(refresh_service, create_test_refresh_token):
    token, _ = await create_test_refresh_token(is_revoked=True, revoked_at=datetime.now(timezone.utc) + timedelta(seconds=15))

    with pytest.raises(RefreshTokenAlreadyRevokedError):
        await refresh_service.revoke_refresh_token(token.id)


@pytest.mark.asyncio
async def test_rotate_refresh_token_success(refresh_service, create_test_refresh_token):
    old_token, _ = await create_test_refresh_token()

    result = await refresh_service.rotate_refresh_token(old_token.id)
    new_token = result.refresh_token

    assert old_token.is_revoked is True
    assert new_token.family_id == old_token.family_id
    assert new_token.parent_token_id == old_token.id


# @pytest.mark.asyncio
# async def test_revoke_token_family(refresh_service, create_test_refresh_token):

#     first_token, _ = await create_test_refresh_token()
#     second_token, _ = await create_test_refresh_token(family_id=first_token.family_id)

#     await refresh_service.revoke_token_family(first_token.family_id)

#     await refresh_service.session.refresh(first_token)
#     await refresh_service.session.refresh(second_token)


#     assert first_token.is_revoked is True
#     assert second_token.is_revoked is True

@pytest.mark.asyncio
async def test_get_refresh_token_by_hash(refresh_service, create_test_refresh_token):
    token, raw_token = await create_test_refresh_token()

    hashed =  refresh_service.security.hash_refresh_token(raw_token)
    result = await refresh_service.get_token_by_hash(hashed)

    assert result.id == token.id


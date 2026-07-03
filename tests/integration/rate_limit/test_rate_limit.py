import pytest

from tests.conftest import API_PREFIX


@pytest.mark.asyncio
async def test_request_under_limit(client, create_test_user):
    user, password = await create_test_user()

    for _ in range(5):
        response = await client.post(
            f"{API_PREFIX}/login", json={"email": user.email, "password": password}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_request_exceed_limit(client, create_test_user):
    user, password = await create_test_user()

    for _ in range(5):
        response = await client.post(
            f"{API_PREFIX}/login", json={"email": user.email, "password": password}
        )
        assert response.status_code == 200

    response = await client.post(
        f"{API_PREFIX}/login", json={"email": user.email, "password": password}
    )
    assert response.status_code == 429

    body = response.json()
    assert body["error"] == "RATE_LIMIT_EXCEEDED"
    assert body["message"] == "Too many requests. Please try again later"

    assert "Retry-After" in response.headers

    retry_after = response.headers["Retry-After"]
    assert int(retry_after) > 0

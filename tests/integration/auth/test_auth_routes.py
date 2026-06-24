import pytest
from tests.conftest import API_PREFIX


@pytest.mark.asyncio
async def test_get_current_user(client, create_test_user):
    user = await create_test_user()
    login = await client.post(f"{API_PREFIX}login", json={"email": user.email, "password": "password"})
    token = login.json()["access_token"]

    response = await client.get(f"{API_PREFIX}/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    body =  response.json()
    assert body["email"] == user.email


@pytest.mark.asyncio
async def tests_register_success(client):
    response = await client.post(f"{API_PREFIX}/register", json={"email":"test1@email.com", "password":"testpass2121"})
    assert response.status_code == 201
    
    body = response.json()
    assert body["email"] == "test1@email.com"

@pytest.mark.asyncio
async def test_login_success(client, create_test_user):
    user = await create_test_user()
    response = await client.post(f"{API_PREFIX}/login", json={"email": user.email, "password": "password"})

    print(response.status_code, response.json())
    
    assert response.status_code == 200
    
    body =  response.json()
    assert "access_token" in body
    assert "refresh_token" in body
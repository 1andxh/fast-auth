import pytest

from src.core.config import settings


# @pytest.mark.asyncio
# async def test_get_current_user(client, create_test_user):
#     user = await create_test_user()
#     token = client.post("/auth")


@pytest.mark.asyncio
async def tests_register_success(client):
    response = await client.post("/auth/register", json={"email":"test1@email.com", "password":"testpass2121"})
    assert response.status_code == 201
    
    body = response.json()
    assert body["email"] == "test1@email.com"

@pytest.mark.asyncio
async def test_login_success(client, create_test_user):
    user = await create_test_user()
    response = await client.post("/auth/login", json={"email": user.email, "password": "password"})
    
    assert response.status_code == 200
    
    body =  response.json()
    assert "access_token" in body
    assert "refresh_token" in body
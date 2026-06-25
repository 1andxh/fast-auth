import pytest
from tests.conftest import API_PREFIX

@pytest.mark.asyncio
async def test_request_id_header_present(client):
    response = await client.get(f"{API_PREFIX}/auth/me", headers={"Authorization": "Bearer Token"})

    assert "X-REQUEST-ID" in response.headers
    assert "X-PROCESS-TIME" in response.headers
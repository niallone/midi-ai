import pytest
from quart import Quart

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get('/health')
    assert response.status_code == 200
    data = await response.get_json()
    assert data == {"status": "healthy", "database": "connected"}

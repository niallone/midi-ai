import pytest
import asyncio
from quart import Quart
from unittest.mock import AsyncMock
from app.src.api import create_api
import jwt
from datetime import datetime, timedelta, timezone

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def asyncio_default_fixture_loop_scope():
    return "session"

@pytest.fixture(scope="module")
async def app() -> Quart:
    app = await create_api()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    return app

@pytest.fixture
async def client(app: Quart):
    async with app.test_client() as test_client:
        yield test_client

@pytest.fixture
async def mock_db():
    mock = AsyncMock()
    mock.fetchval = AsyncMock()
    mock.fetch = AsyncMock()
    mock.fetchrow = AsyncMock()
    mock.execute = AsyncMock()
    return mock

@pytest.fixture
async def admin_token(app: Quart):
    token = jwt.encode({
        'user_id': 1,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token
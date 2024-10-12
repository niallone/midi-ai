"""
This is the top-level conftest file for pytest configuration.
It sets up global pytest plugins and configurations.
"""

import pytest

pytest_plugins = ['pytest_asyncio']

def pytest_configure(config):
    """
    Configure pytest.
    
    This function adds the asyncio marker to pytest configuration.
    """
    config.addinivalue_line(
        "markers", "asyncio: mark test as an asyncio coroutine"
    )

@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the test session.
    
    This fixture creates a new event loop for each test session,
    ensuring proper asyncio behavior across tests.
    
    :yield: An asyncio event loop.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def asyncio_default_fixture_loop_scope():
    """
    Set the default fixture loop scope for asyncio.
    
    This fixture sets the default loop scope to "session" to avoid
    warnings and ensure consistent behavior across tests.
    
    :return: The default fixture loop scope.
    """
    return "session"
"""
This module contains unit tests for the custom error handling in the API.

It tests the behavior of various error types and ensures that they are
properly caught and handled by the application's error handlers.

The tests cover:
- APIError and its subclasses
- Error handler registration
- JSON responses for different error types
- Unexpected errors

Usage:
    Run these tests using pytest:
    $ pytest tests/test_error_handling.py

Note:
    These tests use Quart's test client for asynchronous testing.
    Make sure to use the 'pytest-asyncio' plugin when running the tests.
"""

import pytest
from quart import Quart, jsonify
from app.src.errors import (
    APIError, NotFoundError, BadRequestError, MethodNotAllowedError,
    DatabaseError, AuthenticationError, AuthorisationError, ValidationError
)
from app.src.errors.handlers import register_error_handlers

@pytest.fixture
def app():
    """
    Create a Quart app instance with registered error handlers.

    This fixture provides a fresh Quart app instance for each test,
    with all custom error handlers properly registered.

    Returns:
        Quart: A Quart application instance with error handlers.
    """
    app = Quart(__name__)
    register_error_handlers(app)
    return app

@pytest.mark.asyncio
async def test_api_error(app):
    """
    Test handling of the base APIError.

    This test ensures that a generic APIError is correctly caught
    and returns the expected JSON response.
    """
    @app.route('/test-api-error')
    async def test_route():
        raise APIError("Test API Error", status_code=400)

    async with app.test_client() as client:
        response = await client.get('/test-api-error')
        assert response.status_code == 400
        data = await response.get_json()
        assert data['message'] == "Test API Error"

@pytest.mark.asyncio
async def test_not_found_error(app):
    """
    Test handling of NotFoundError.

    Ensures that NotFoundError is caught and returns a 404 status
    with the correct error message.
    """
    @app.route('/test-not-found')
    async def test_route():
        raise NotFoundError("Resource not found")

    async with app.test_client() as client:
        response = await client.get('/test-not-found')
        assert response.status_code == 404
        data = await response.get_json()
        assert data['message'] == "Resource not found"

@pytest.mark.asyncio
async def test_bad_request_error(app):
    """
    Test handling of BadRequestError.

    Verifies that BadRequestError is caught and returns a 400 status
    with the appropriate error message.
    """
    @app.route('/test-bad-request')
    async def test_route():
        raise BadRequestError("Invalid input")

    async with app.test_client() as client:
        response = await client.get('/test-bad-request')
        assert response.status_code == 400
        data = await response.get_json()
        assert data['message'] == "Invalid input"

@pytest.mark.asyncio
async def test_method_not_allowed_error(app):
    """
    Test handling of MethodNotAllowedError.

    Checks if MethodNotAllowedError is caught and returns a 405 status
    with the correct error message.
    """
    @app.route('/test-method-not-allowed', methods=['GET'])
    async def test_route():
        return jsonify({"message": "This is a GET route"})

    async with app.test_client() as client:
        response = await client.post('/test-method-not-allowed')
        assert response.status_code == 405
        data = await response.get_json()
        assert "message" in data
        assert "method is not allowed" in data['message'].lower()

@pytest.mark.asyncio
async def test_database_error(app):
    """
    Test handling of DatabaseError.

    Ensures that DatabaseError is caught and returns a 500 status
    with the appropriate error message.
    """
    @app.route('/test-database-error')
    async def test_route():
        raise DatabaseError("Database connection failed")

    async with app.test_client() as client:
        response = await client.get('/test-database-error')
        assert response.status_code == 500
        data = await response.get_json()
        assert data['message'] == "Database connection failed"

@pytest.mark.asyncio
async def test_authentication_error(app):
    """
    Test handling of AuthenticationError.

    Verifies that AuthenticationError is caught and returns a 401 status
    with the correct error message.
    """
    @app.route('/test-authentication-error')
    async def test_route():
        raise AuthenticationError("Invalid credentials")

    async with app.test_client() as client:
        response = await client.get('/test-authentication-error')
        assert response.status_code == 401
        data = await response.get_json()
        assert data['message'] == "Invalid credentials"

@pytest.mark.asyncio
async def test_authorisation_error(app):
    """
    Test handling of AuthorisationError.

    Checks if AuthorisationError is caught and returns a 403 status
    with the appropriate error message.
    """
    @app.route('/test-authorisation-error')
    async def test_route():
        raise AuthorisationError("Insufficient permissions")

    async with app.test_client() as client:
        response = await client.get('/test-authorisation-error')
        assert response.status_code == 403
        data = await response.get_json()
        assert data['message'] == "Insufficient permissions"

@pytest.mark.asyncio
async def test_validation_error(app):
    """
    Test handling of ValidationError.

    Ensures that ValidationError is caught and returns a 422 status
    with the correct error message.
    """
    @app.route('/test-validation-error')
    async def test_route():
        raise ValidationError("Invalid data format")

    async with app.test_client() as client:
        response = await client.get('/test-validation-error')
        assert response.status_code == 422
        data = await response.get_json()
        assert data['message'] == "Invalid data format"

@pytest.mark.asyncio
async def test_unexpected_error(app):
    """
    Test handling of unexpected errors.

    Verifies that unexpected exceptions are caught by the default handler
    and return a 500 status with a generic error message.
    """
    @app.route('/test-unexpected-error')
    async def test_route():
        raise Exception("Unexpected error")

    async with app.test_client() as client:
        response = await client.get('/test-unexpected-error')
        assert response.status_code == 500
        data = await response.get_json()
        assert data['error'] == "An unexpected error occurred."
        assert data['type'] == "Exception"


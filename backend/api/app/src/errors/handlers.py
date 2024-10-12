"""
This module contains functions for registering error handlers with the Quart application.

It defines how different types of errors should be handled and formatted in API responses.
"""

from quart import jsonify
import logging
import traceback
from .api import APIError
from .http import NotFoundError, BadRequestError, MethodNotAllowedError
from .database import DatabaseError
from .auth import AuthenticationError, AuthorisationError
from .validation import ValidationError

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """
    Register error handlers for the Quart application.

    This function sets up handlers for specific error types, `APIError`, and general exceptions.
    It ensures that all errors are returned in a consistent JSON format.

    Args:
        app (Quart): The Quart application instance.

    Note:
        This function should be called after the Quart app is created,
        typically in the app factory or initialization code.
    """

    @app.errorhandler(NotFoundError)
    async def handle_not_found_error(error):
        """Handle `NotFoundError` exceptions by returning a 404 response with a JSON payload."""
        return jsonify(error.to_dict()), 404

    @app.errorhandler(BadRequestError)
    async def handle_bad_request_error(error):
        """Handle `BadRequestError` exceptions by returning a 400 response with a JSON payload."""
        return jsonify(error.to_dict()), 400

    @app.errorhandler(MethodNotAllowedError)
    async def handle_method_not_allowed_error(error):
        """Handle `MethodNotAllowedError` exceptions by returning a 405 response with a JSON payload."""
        return jsonify(error.to_dict()), 405

    @app.errorhandler(DatabaseError)
    async def handle_database_error(error):
        """Handle `DatabaseError` exceptions by returning a 500 response with a JSON payload."""
        return jsonify(error.to_dict()), 500

    @app.errorhandler(AuthenticationError)
    async def handle_authentication_error(error):
        """Handle `AuthenticationError` exceptions by returning a 401 response with a JSON payload."""
        return jsonify(error.to_dict()), 401

    @app.errorhandler(AuthorisationError)
    async def handle_authorisation_error(error):
        """Handle `AuthorisationError` exceptions by returning a 403 response with a JSON payload."""
        return jsonify(error.to_dict()), 403

    @app.errorhandler(ValidationError)
    async def handle_validation_error(error):
        """Handle `ValidationError` exceptions by returning a 422 response with a JSON payload."""
        return jsonify(error.to_dict()), 422

    @app.errorhandler(APIError)
    async def handle_api_error(error):
        """
        Handle `APIError` exceptions.

        This handler catches all `APIError` instances and returns them
        as JSON responses with the appropriate status code.

        Args:
            error (APIError): The caught `APIError` instance.

        Returns:
            Response: A Quart JSON response with the error details and status code.
        """
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    async def handle_unexpected_error(error):
        """
        Handle unexpected exceptions.

        This is a catch-all handler for any exceptions that are not `APIError` instances.
        It logs the error and returns a generic error message to avoid
        exposing sensitive information.

        Args:
            error (Exception): The caught exception.

        Returns:
            Response: A Quart JSON response with a generic error message and a 500 status code.
        """
        logger.exception('An unexpected error occurred.')
        error_details = {
            'error': 'An unexpected error occurred.',
            'type': str(type(error).__name__),
            'message': str(error),
            'traceback': traceback.format_exc()
        }
        return jsonify(error_details), 500

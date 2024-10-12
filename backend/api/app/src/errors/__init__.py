"""
This package contains custom error classes and error handling utilities for the API.

It provides a set of specific error types for different scenarios in the application,
allowing for more precise error handling and reporting.

Modules:
- api: Defines the base APIError class.
- http: Contains HTTP-specific error classes.
- database: Defines database-related error classes.
- auth: Provides authentication and authorisation error classes.
- handlers: Contains functions for registering error handlers with the Quart app.

Usage:
    from app.src.errors import APIError, NotFoundError, DatabaseError, AuthenticationError
"""

from .api import APIError
from .http import NotFoundError, BadRequestError, MethodNotAllowedError
from .database import DatabaseError
from .auth import AuthenticationError, AuthorisationError
from .validation import ValidationError
from .handlers import register_error_handlers

__all__ = [
    'APIError',
    'NotFoundError',
    'BadRequestError',
    'MethodNotAllowedError',
    'DatabaseError',
    'AuthenticationError',
    'AuthorisationError',
    'ValidationError',
    'register_error_handlers'
]
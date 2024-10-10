from flask import jsonify

class APIError(Exception):
    """Base exception class for API errors."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def register_error_handlers(app):
    """
    Register custom error handlers for the Flask application.

    This function sets up custom error handlers for various HTTP error codes
    and the custom APIError exception. It ensures that all errors are returned
    in a consistent JSON format.

    Args:
        app: The Flask application instance.

    Returns:
        None
    """

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom APIError exceptions."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle 400 Bad Request errors."""
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f"An internal error occurred: {str(error)}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500

    # Add more error handlers as needed
    # For example:
    # @app.errorhandler(403)
    # def forbidden_error(error):
    #     return jsonify({"error": "Forbidden", "message": "You don't have permission to access this resource."}), 403
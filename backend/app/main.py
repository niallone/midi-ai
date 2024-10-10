from flask import Flask
from flask_cors import CORS
from .config import Config
from .api.routes import api_bp
from .db.database import init_db
from .core.exceptions import register_error_handlers

def create_app(config_class=Config):
    """
    Create and configure an instance of the Flask application.

    This function sets up the Flask app with all necessary extensions,
    blueprints, and configurations. It's designed to be flexible,
    allowing for different configurations to be passed in, which is
    particularly useful for testing.

    Args:
        config_class: The configuration class to use. Defaults to Config.

    Returns:
        A configured Flask application instance.
    """
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Load the configurations from the config class
    app.config.from_object(config_class)

    # Initialize Cross-Origin Resource Sharing (CORS)
    # This allows the API to be accessed from different domains
    allowed_origins = {"https://melodygenerator.fun", "http://localhost:3000"}

    CORS(app, 
        resources={r"/*": {"origins": list(allowed_origins)}},
        supports_credentials=True
    )

    # Initialize the database connection
    init_db(app)

    # Register the API blueprint
    # This sets up all the routes for our API under the '/api' prefix
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register custom error handlers
    # This ensures that errors are handled gracefully and return appropriate responses
    register_error_handlers(app)

    return app


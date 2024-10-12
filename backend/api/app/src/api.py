import os
import asyncio
from quart import Quart, request
from quart_cors import cors
from quart_auth import QuartAuth
from app.database.postgres.database import pg_db
from app.src.errors.handlers import register_error_handlers
from app.src.routes import routes_bp
from app.src.utils.logging import setup_logging
from app.src.services.melody_generator import get_available_models

async def create_api():
    """
    Create and configure the Quart application.

    This function sets up the Quart app, configures CORS, sets up logging,
    initializes the database connection, preloads models, and registers the routes.

    Returns:
        Quart: Configured Quart application
    """
    # Create a new Quart application
    api = Quart(__name__)
    
    # Set up configuration variables
    api.config['MODEL_DIR'] = os.environ.get('MODEL_DIR', '/usr/src/api/app/model')
    api.config['OUTPUT_DIR'] = os.environ.get('OUTPUT_DIR', '/usr/src/api/app/output')

    # Enable CORS for the application
    allowed_origins = {"https://melodygenerator.fun", "http://localhost:3000"}

    # Configure CORS with quart_cors
    api = cors(
        api, 
        allow_origin=allowed_origins,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        allow_credentials=True,
        # expose_headers="Access-Control-Allow-Origin"
    )

    # # Add CORS headers to all responses
    # @api.after_request
    # def add_cors_headers(response):
    #     origin = request.headers.get('Origin')
    #     if origin in allowed_origins:
    #         response.headers['Access-Control-Allow-Origin'] = origin
    #     response.headers['Access-Control-Allow-Credentials'] = 'true'
    #     return response

    # Configure logging
    setup_logging(api)

    # The secret key for JWT
    api.config['SECRET_KEY'] = 'DLeeL345jympT4b9ybPkhtGENK' 

    # Initialize Quart-Auth
    QuartAuth(api)

    @api.before_serving
    async def startup_tasks():
        """
        Perform startup tasks before the app starts serving requests.

        This includes initializing the database connection and preloading models.
        """
        # Initialize the database connection
        api.pg_db = await pg_db.get_instance()

        # Preload and cache the melody generation models
        api.logger.info("Preloading melody generation models")
        try:
            models = await get_available_models()
            api.config['MODELS'] = models
            api.logger.info(f"Loaded models: {list(models.keys())}")
        except Exception as e:
            api.logger.error(f"Error preloading models: {str(e)}")

    @api.after_serving
    async def shutdown_tasks():
        """
        Perform shutdown tasks after the app stops serving requests.

        This includes closing the database connection.
        """
        # Close the database connection
        if hasattr(api, 'pg_db'):
            await api.pg_db.close()
            api.logger.info("Database connection closed")

    # Register error handlers
    register_error_handlers(api)

    # Register the routes blueprint
    api.register_blueprint(routes_bp)

    return api

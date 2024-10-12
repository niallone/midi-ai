import os
from quart import Quart, request
from quart_cors import cors
from quart_auth import QuartAuth
from app.database.postgres.database import pg_db
from app.src.errors.handlers import register_error_handlers
from app.src.routes import routes_bp
from app.src.utils.logging import setup_logging

async def create_api():
    """
    Create and configure the Quart application.

    This function sets up the Quart app, configures CORS, sets up logging,
    initialises the database connection, and registers the routes.

    :return: Configured Quart application
    """
    # Create a new Quart application
    api = Quart(__name__)
    
    api.config['MODEL_DIR'] = os.environ.get('MODEL_DIR', '/usr/src/api/app/model')
    api.config['OUTPUT_DIR'] = os.environ.get('OUTPUT_DIR', '/usr/src/api/app/output')

    # Enable CORS routes for the application
    allowed_origins = {"https://melodygenerator.fun", "http://localhost:3000"}
    
    # Configure CORS with the callable
    api = cors(api, 
        allow_origins=allowed_origins,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        allow_credentials=True,
        expose_headers="Access-Control-Allow-Origin"
    )
    
    # Add CORS headers to all responses
    @api.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    # Configure logging
    setup_logging(api)

    # The secret key for the JWT
    api.config['SECRET_KEY'] = 'DLeeL345jympT4b9ybPkhtGENK' 
    
    # Initialise AuthManager
    QuartAuth(api)
    
    @api.before_serving
    async def setup_db():
        """
        Initialise the database connection before the app starts serving requests.
        """
        api.pg_db = await pg_db.get_instance()

    @api.after_serving
    async def close_db():
        """
        Close the database connection after the app stops serving requests.
        """
        await api.pg_db
        pg_db.close()

    # Debugging middleware
    # @api.before_request
    # async def log_request_info():
    #     api.logger.debug('Request Origin: %s', request.headers.get('Origin'))

    # Register error handlers
    register_error_handlers(api)

    # Register the routes blueprint
    api.register_blueprint(routes_bp)

    return api

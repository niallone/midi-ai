import logging
from quart import request

def setup_logging(app):
    logging.basicConfig(level=logging.INFO)
    app.logger = logging.getLogger(__name__)

    @app.before_request
    async def log_request_info():
        app.logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    async def log_response_info(response):
        app.logger.info(f"Response: {response.status}")
        return response
from quart import Blueprint, jsonify, current_app, request
from app.src.errors.api import APIError

bp = Blueprint('main', __name__)

@bp.route('/health', methods=['GET'])
async def health_check():
    try:
        # Attempt to fetch a single value from the database
        result = await current_app.pg_db.fetchval("SELECT 1")
        if result == 1:
            return jsonify({"status": "healthy", "database": "connected"}), 200
        else:
            return jsonify({"status": "unhealthy", "database": "error", "message": "Database health check failed"}), 500
    except Exception as e:
        current_app.logger.error(f"Database health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "database": "error", "message": "Database health check failed"}), 500

@bp.route('/')
async def index():
    try:
        # Return text response
        return f"Welcome to the Melodygenerator API."
    except Exception as e:
        current_app.logger.error(f"Error in index route: {str(e)}")
        return jsonify({"error": "An error occurred while fetching user count"}), 500

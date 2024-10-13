from quart import Blueprint, jsonify, current_app
from app.src.utils.auth import token_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/test', methods=['GET'])
@token_required
async def test():
    try:
        # Return text response
        return "Welcome to the Admin API."
    except Exception as e:
        current_app.logger.error(f"Error in test route: {str(e)}")
        return jsonify({"error": "An error occurred in the test route"}), 500
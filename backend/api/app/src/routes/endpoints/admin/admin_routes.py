from quart import Blueprint, jsonify, current_app
from app.src.utils.auth import token_required

admin_bp = Blueprint('admin', __name__)

# Other admin related routes
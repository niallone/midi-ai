from quart import Blueprint
from .main import bp as main_bp
from .endpoints.auth.auth_routes import auth_bp
from .endpoints.admin.admin_routes import admin_bp
from .endpoints.user.user_account_routes import user_account_bp
from .endpoints.melody.melody import melody_bp

# Create a main routes blueprint
routes_bp = Blueprint('routes', __name__)

# Register all sub-blueprints
routes_bp.register_blueprint(main_bp)
routes_bp.register_blueprint(auth_bp, url_prefix='/auth')
routes_bp.register_blueprint(admin_bp, url_prefix='/admin')
routes_bp.register_blueprint(melody_bp, url_prefix='/melody')

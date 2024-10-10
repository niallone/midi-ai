from flask import Blueprint
from app.api.endpoints import models, melodies

# Create a Blueprint for our API
# This allows us to organise a group of related routes
api_bp = Blueprint('api', __name__)

# Define the routes for our API
# Each route is associated with a specific function in our endpoints

# Route for getting available models
# GET /api/models
api_bp.add_url_rule('/models', view_func=models.get_models, methods=['GET'])

# Route for generating a new melody
# POST /api/generate
api_bp.add_url_rule('/generate', view_func=melodies.generate_melody, methods=['POST'])

# Route for downloading a generated melody file
# GET /api/download/<filename>
api_bp.add_url_rule('/download/<filename>', view_func=melodies.download_file, methods=['GET'])

# Additional routes can be added here as the API expands
# For example:
# api_bp.add_url_rule('/users', view_func=users.get_users, methods=['GET'])
# api_bp.add_url_rule('/users/<int:user_id>', view_func=users.get_user, methods=['GET'])
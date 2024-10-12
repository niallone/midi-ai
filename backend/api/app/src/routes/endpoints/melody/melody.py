import os
import traceback
from quart import Blueprint, jsonify, request, send_from_directory, current_app
from app.src.services.melody_generator import generate_melody as generate_melody_service
from app.src.services.melody_generator import get_available_models

melody_bp = Blueprint('melody', __name__)



@melody_bp.route('/test', methods=['GET'])
async def test():
    try:
        # Return text response
        return f"Welcome to the Melodygenerator API."
    except Exception as e:
        current_app.logger.error(f"Error in index route: {str(e)}")
        return jsonify({"error": "An error occurred while fetching user count"}), 500

@melody_bp.route('/models', methods=['GET'])
async def get_models():
    """
    Retrieve and return a list of available melody generation models.
    """
    try:
        current_app.logger.debug("Entering get_models route handler")
        current_app.logger.debug(f"Current app config: {current_app.config}")
        models = await get_available_models()
        current_app.logger.debug(f"Models retrieved: {models}")
        model_list = [{'id': model_id, 'name': model_id} for model_id in models.keys()]
        current_app.logger.debug(f"Returning model list: {model_list}")
        return jsonify(model_list)
    except Exception as e:
        current_app.logger.error(f"Error fetching models: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"An error occurred while fetching models: {str(e)}"}), 500

@melody_bp.route('/generate', methods=['POST'])
async def generate_melody():
    """
    Generate a new melody based on the provided model ID.
    """
    try:
        current_app.logger.debug("Entering generate_melody endpoint")
        data = await request.get_json()
        model_id = data.get('model_id')

        current_app.logger.debug(f"Received request with model_id: {model_id}")

        if not model_id:
            current_app.logger.error("No model_id provided")
            return jsonify({"error": "No model_id provided"}), 400

        current_app.logger.debug(f"Calling generate_melody_service with model_id: {model_id}")
        output_file = await generate_melody_service(model_id)

        current_app.logger.debug(f"Generated melody file: {output_file}")

        return jsonify({
            "message": "Melody generated successfully",
            "file_name": os.path.basename(output_file)
        }), 200
    except ValueError as ve:
        current_app.logger.error(f"ValueError in generate_melody: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Error generating melody: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": "An unexpected error occurred while generating the melody"}), 500

@melody_bp.route('/download/<filename>', methods=['GET'])
async def download_file(filename):
    """
    Serve a generated melody file for download.
    """
    try:
        return await send_from_directory(current_app.config['OUTPUT_DIR'], filename, as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Error downloading file {filename}: {str(e)}")
        return jsonify({"error": "File not found"}), 404
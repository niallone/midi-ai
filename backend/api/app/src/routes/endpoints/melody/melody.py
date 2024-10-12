import asyncio
import os
import traceback
from quart import Blueprint, jsonify, request, send_from_directory, current_app
from app.src.services.melody_generator import generate_melody as generate_melody_service
from app.src.services.melody_generator import get_available_models

melody_bp = Blueprint('melody', __name__)

@melody_bp.route('/test', methods=['GET'])
async def test():
    """
    A simple test endpoint to verify the API is working.

    Returns:
        str: A welcome message.
    """
    try:
        # Return text response
        return "Welcome to the Melodygenerator API."
    except Exception as e:
        current_app.logger.error(f"Error in test route: {str(e)}")
        return jsonify({"error": "An error occurred in the test route"}), 500

@melody_bp.route('/models', methods=['GET'])
async def get_models():
    """
    Retrieve and return a list of available melody generation models.

    Returns:
        JSON: A list of available models.
    """
    try:
        current_app.logger.debug("Entering get_models route handler")
        current_app.logger.debug(f"Current app config: {current_app.config}")

        # Retrieve the cached models from the app config
        models = current_app.config.get('MODELS')
        if not models:
            # If models are not cached, load them
            current_app.logger.info("Models not cached, loading models")
            models = await get_available_models()
            current_app.config['MODELS'] = models

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

    Expects:
        JSON payload with 'model_id' field.

    Returns:
        JSON: A message and the filename of the generated melody.
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

        # Run the melody generation in a separate thread to avoid blocking the event loop
        output_file = await asyncio.to_thread(_generate_and_save_melody, model_id)

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

def _generate_and_save_melody(model_id):
    """
    Synchronous wrapper function to generate and save the melody.

    This function runs in a separate thread using asyncio.to_thread
    to avoid blocking the main event loop.

    Args:
        model_id (str): The ID of the model to use for generation.

    Returns:
        str: The path to the generated melody file.
    """
    # Since this function is running in a separate thread, we can create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Call the asynchronous generate_melody_service function
        output_file = loop.run_until_complete(generate_melody_service(model_id))
    finally:
        loop.close()
    return output_file

@melody_bp.route('/download/<filename>', methods=['GET'])
async def download_file(filename):
    """
    Serve a generated melody file for download.

    Args:
        filename (str): The name of the file to download.

    Returns:
        The requested file as an attachment.
    """
    try:
        return await send_from_directory(
            current_app.config['OUTPUT_DIR'], filename, as_attachment=True
        )
    except Exception as e:
        current_app.logger.error(f"Error downloading file {filename}: {str(e)}")
        return jsonify({"error": "File not found"}), 404

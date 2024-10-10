import os
from flask import jsonify, request, send_from_directory, current_app
from app.services.melody_generator import generate_melody as generate_melody_service

def generate_melody():
    """
    Generate a new melody based on the provided model ID.

    This function expects a JSON payload with a 'model_id' field. It uses
    the specified model to generate a new melody, saves it to a file,
    and returns the filename of the generated melody.

    Returns:
        A JSON response containing a success message and the filename
        of the generated melody. If an error occurs, it returns a JSON
        object with an 'error' field and an appropriate status code.

    Example request:
        POST /api/generate
        Content-Type: application/json
        {
            "model_id": "model1"
        }

    Example response:
        {
            "message": "Melody generated successfully",
            "file_name": "generated_melody_1234567890.mid"
        }
    """
    try:
        # Extract the model_id from the request JSON
        data = request.get_json()
        model_id = data.get('model_id')

        # Validate the model_id
        if not model_id:
            return jsonify({"error": "No model_id provided"}), 400

        # Generate the melody using the service function
        output_file = generate_melody_service(model_id)

        # Return a success response with the generated file name
        return jsonify({
            "message": "Melody generated successfully",
            "file_name": os.path.basename(output_file)
        }), 200

    except ValueError as ve:
        # Handle validation errors
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Log unexpected errors and return a generic error message
        current_app.logger.error(f"Error generating melody: {str(e)}")
        return jsonify({"error": "An unexpected error occurred while generating the melody"}), 500

def download_file(filename):
    """
    Serve a generated melody file for download.

    This function attempts to send the requested file from the
    OUTPUT_DIR directory as an attachment.

    Args:
        filename (str): The name of the file to download.

    Returns:
        The requested file as an attachment if found, or a JSON error
        response if the file is not found or an error occurs.

    Example usage:
        GET /api/download/generated_melody_1234567890.mid
    """
    try:
        # Attempt to send the requested file from the OUTPUT_DIR
        return send_from_directory(current_app.config['OUTPUT_DIR'], filename, as_attachment=True)

    except Exception as e:
        # Log the error and return a file not found error response
        current_app.logger.error(f"Error downloading file {filename}: {str(e)}")
        return jsonify({"error": "File not found"}), 404
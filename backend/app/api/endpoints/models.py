from flask import jsonify, current_app
from app.services.melody_generator import get_available_models

def get_models():
    """
    Retrieve and return a list of available melody generation models.

    This function fetches the list of available models from the melody
    generator service and returns it as a JSON response. Each model is
    represented by an object containing its ID and name.

    Returns:
        A JSON response containing a list of model objects, each with
        'id' and 'name' fields. If an error occurs, it returns a JSON
        object with an 'error' field and a 500 status code.

    Example response:
        [
            {"id": "model1", "name": "model1"},
            {"id": "model2", "name": "model2"}
        ]
    """
    try:
        # Fetch available models from the melody generator service
        models = get_available_models()

        # Convert the models dictionary to a list of objects
        model_list = [{'id': model_id, 'name': model_id} for model_id in models.keys()]

        # Return the list of models as a JSON response
        return jsonify(model_list)

    except Exception as e:
        # Log the error for debugging purposes
        current_app.logger.error(f"Error fetching models: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching models"}), 500
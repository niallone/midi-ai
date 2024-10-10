import os
import time
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from melody_generator import generate_melody, create_midi
from model_trainer import load_or_train_model

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load environment variables
MIDI_DIR = os.environ.get('MIDI_DIR', '/app/input')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')
MODEL_DIR = os.environ.get('MODEL_DIR', '/app/model')

logger.info(f"MIDI_DIR: {MIDI_DIR}")
logger.info(f"OUTPUT_DIR: {OUTPUT_DIR}")
logger.info(f"MODEL_DIR: {MODEL_DIR}")

# Load available models
models = {}
logger.info(f"Searching for model files in: {MODEL_DIR}")
if os.path.exists(MODEL_DIR):
    for filename in os.listdir(MODEL_DIR):
        if filename.endswith('.h5'):
            model_id = os.path.splitext(filename)[0]
            model_path = os.path.join(MODEL_DIR, filename)
            logger.info(f"Found model file: {model_path}")
            try:
                models[model_id] = load_or_train_model(MIDI_DIR, model_path)
                logger.info(f"Successfully loaded model: {model_id}")
            except Exception as e:
                logger.error(f"Error loading model {model_id}: {str(e)}")
else:
    logger.error(f"MODEL_DIR does not exist: {MODEL_DIR}")

@app.route('/api/models', methods=['GET'])
def get_models():
    logger.info(f"Received request for /api/models")
    logger.info(f"Available models: {list(models.keys())}")
    return jsonify([{'id': model_id, 'name': model_id} for model_id in models.keys()])

@app.route('/generate', methods=['POST'])
def generate_melody_api():
    try:
        data = request.get_json()
        logger.info(f"Received generation request with data: {data}")

        model_id = data.get('model_id')
        if not model_id:
            logger.error("No model_id provided in the request")
            return jsonify({"error": "No model_id provided"}), 400

        if model_id not in models:
            logger.error(f"Invalid model ID: {model_id}")
            return jsonify({"error": f"Invalid model ID: {model_id}"}), 400

        model, network_input, pitchnames, note_to_int, n_vocab = models[model_id]
        generated_notes = generate_melody(model, network_input, pitchnames, note_to_int, n_vocab)
        output_file = os.path.join(OUTPUT_DIR, f"generated_melody_{int(time.time())}.mid")
        create_midi(generated_notes, filename=output_file)
        logger.info(f"Melody generated successfully: {output_file}")
        return jsonify({
            "message": "Melody generated successfully",
            "file_name": os.path.basename(output_file)
        }), 200
    except Exception as e:
        logger.error(f"Error generating melody: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    logger.info(f"Received download request for file: {filename}")
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host='0.0.0.0', port=4050)
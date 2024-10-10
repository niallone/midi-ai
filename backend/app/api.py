import os
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from tensorflow.keras.models import load_model
import pickle
from melody_generator import generate_melody, create_midi

app = Flask(__name__)
CORS(app)

# Load environment variables
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')
MODEL_DIR = os.environ.get('MODEL_DIR', '/app/model')

def load_model_data(model_path):
    model = load_model(model_path)
    data_path = f"{model_path}_data.pkl"
    
    with open(data_path, "rb") as f:
        network_input, pitchnames, note_to_int, n_vocab = pickle.load(f)
    
    return model, network_input, pitchnames, note_to_int, n_vocab

# Load available models
models = {}
for filename in os.listdir(MODEL_DIR):
    if filename.endswith('.h5'):
        model_id = os.path.splitext(filename)[0]
        model_path = os.path.join(MODEL_DIR, filename)
        try:
            models[model_id] = load_model_data(model_path)
            print(f"Loaded model: {model_id}")
        except Exception as e:
            print(f"Error loading model {model_id}: {str(e)}")

@app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify([{'id': model_id, 'name': model_id} for model_id in models.keys()])

@app.route('/generate', methods=['POST'])
def generate_melody_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided in the request"}), 400

        model_id = data.get('model_id')
        if not model_id:
            return jsonify({"error": "No model_id provided in the request"}), 400

        if model_id not in models:
            return jsonify({"error": f"Invalid model ID: {model_id}"}), 400

        model, network_input, pitchnames, note_to_int, n_vocab = models[model_id]
        generated_notes = generate_melody(model, network_input, pitchnames, note_to_int, n_vocab)
        output_file = os.path.join(OUTPUT_DIR, f"generated_melody_{int(time.time())}.mid")
        create_midi(generated_notes, filename=output_file)
        return jsonify({
            "message": "Melody generated successfully",
            "file_name": os.path.basename(output_file)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4050)
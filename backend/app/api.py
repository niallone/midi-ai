import os
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from melody_generator import generate_melody, create_midi
from model_trainer import load_or_train_model

app = Flask(__name__)
CORS(app)

print("Flask app is starting up!", flush=True)

# Load environment variables
MIDI_DIR = os.environ.get('MIDI_DIR', '/app/input')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')
MODEL_DIR = os.environ.get('MODEL_DIR', '/app/model')

print(f"MIDI_DIR: {MIDI_DIR}", flush=True)
print(f"OUTPUT_DIR: {OUTPUT_DIR}", flush=True)
print(f"MODEL_DIR: {MODEL_DIR}", flush=True)

# Load available models
models = {}
print(f"Searching for model files in: {MODEL_DIR}", flush=True)
if os.path.exists(MODEL_DIR):
    for filename in os.listdir(MODEL_DIR):
        if filename.endswith('.h5'):
            model_id = os.path.splitext(filename)[0]
            model_path = os.path.join(MODEL_DIR, filename)
            print(f"Found model file: {model_path}", flush=True)
            try:
                models[model_id] = load_or_train_model(MIDI_DIR, model_path)
                print(f"Successfully loaded model: {model_id}", flush=True)
            except Exception as e:
                print(f"Error loading model {model_id}: {str(e)}", flush=True)
else:
    print(f"MODEL_DIR does not exist: {MODEL_DIR}", flush=True)

@app.route('/api/models', methods=['GET'])
def get_models():
    print(f"Received request for /api/models", flush=True)
    print(f"Available models: {list(models.keys())}", flush=True)
    return jsonify([{"id":"melody_generator_lstm_v3","name":"melody_generator_lstm_v3"},{"id":"melody_generator_lstm_v2","name":"melody_generator_lstm_v2"},{"id":"trained_model","name":"trained_model"}])
    #return jsonify([{'id': model_id, 'name': model_id} for model_id in models.keys()])

@app.route('/generate', methods=['POST'])
def generate_melody_api():
    try:
        data = request.get_json()
        print(f"Received generation request with data: {data}", flush=True)

        model_id = data.get('model_id')
        if not model_id:
            print("No model_id provided in the request", flush=True)
            return jsonify({"error": "No model_id provided"}), 400

        if model_id not in models:
            print(f"Invalid model ID: {model_id}", flush=True)
            return jsonify({"error": f"Invalid model ID: {model_id}"}), 400

        model, network_input, pitchnames, note_to_int, n_vocab = models[model_id]
        generated_notes = generate_melody(model, network_input, pitchnames, note_to_int, n_vocab)
        output_file = os.path.join(OUTPUT_DIR, f"generated_melody_{int(time.time())}.mid")
        create_midi(generated_notes, filename=output_file)
        print(f"Melody generated successfully: {output_file}", flush=True)
        return jsonify({
            "message": "Melody generated successfully",
            "file_name": os.path.basename(output_file)
        }), 200
    except Exception as e:
        print(f"Error generating melody: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    print(f"Received download request for file: {filename}", flush=True)
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    print("Starting Flask application", flush=True)
    app.run(host='0.0.0.0', port=4050)
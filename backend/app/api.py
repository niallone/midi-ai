import os
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from melody_generator import generate_melody, create_midi
from model_trainer import load_or_train_model

app = Flask(__name__)
CORS(app)

# Load environment variables
MIDI_DIR = os.environ.get('MIDI_DIR', '/app/input')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')
MODEL_PATH = os.environ.get('MODEL_PATH', '/app/model/melody_generator_lstm_v1.h5')

print(f"Debug: MIDI_DIR = {MIDI_DIR}", flush=True)
print(f"Debug: OUTPUT_DIR = {OUTPUT_DIR}", flush=True)
print(f"Debug: MODEL_PATH = {MODEL_PATH}", flush=True)

# Load or train the model
print("Debug: About to call load_or_train_model", flush=True)
model, network_input, pitchnames, note_to_int, n_vocab = load_or_train_model(MIDI_DIR, MODEL_PATH)
print("Debug: Finished load_or_train_model", flush=True)

@app.route('/generate', methods=['POST'])
def generate_melody_api():
    try:
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
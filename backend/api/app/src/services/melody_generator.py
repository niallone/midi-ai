import os
import time
import pickle
import traceback
import json
import asyncio
import numpy as np
from quart import current_app
from tensorflow import keras
from tensorflow.keras import layers
from music21 import instrument, note, stream, chord

def custom_load_model(filepath):
    """Custom model loading function to handle potential version incompatibilities."""
    import h5py
    
    def remove_time_major(config):
        if isinstance(config, dict):
            return {k: remove_time_major(v) for k, v in config.items() if k != 'time_major'}
        elif isinstance(config, list):
            return [remove_time_major(item) for item in config]
        else:
            return config

    with h5py.File(filepath, mode='r') as f:
        model_config = f.attrs.get('model_config')
        if isinstance(model_config, bytes):
            model_config = model_config.decode('utf-8')
        model_config = json.loads(model_config)
        
    # Remove 'time_major' from the entire model configuration
    cleaned_config = remove_time_major(model_config)
    
    # Create model from cleaned config
    model = keras.models.model_from_json(json.dumps(cleaned_config))
    
    # Load weights
    model.load_weights(filepath)
    
    return model

def custom_load_model(filepath):
    """Custom model loading function to handle potential version incompatibilities."""
    import h5py
    
    def create_layer(layer_config):
        layer_class = getattr(keras.layers, layer_config['class_name'])
        return layer_class.from_config(layer_config['config'])

    with h5py.File(filepath, mode='r') as f:
        model_config = f.attrs.get('model_config')
        if isinstance(model_config, bytes):
            model_config = model_config.decode('utf-8')
        model_config = json.loads(model_config)

    # Create a new Sequential model
    model = keras.Sequential()

    # Add layers to the model
    for layer_config in model_config['config']['layers']:
        if layer_config['class_name'] != 'InputLayer':
            model.add(create_layer(layer_config))

    # Load weights
    model.load_weights(filepath)

    return model

async def get_available_models():
    current_app.logger.debug("Entering get_available_models function")
    current_app.logger.debug(f"Current app config: {current_app.config}")

    if 'MODEL_DIR' not in current_app.config:
        current_app.logger.error("MODEL_DIR not found in app config")
        raise KeyError("MODEL_DIR configuration is missing")

    model_dir = current_app.config['MODEL_DIR']
    current_app.logger.info(f"Loading models from {model_dir}")

    if not os.path.exists(model_dir):
        current_app.logger.error(f"Model directory does not exist: {model_dir}")
        raise FileNotFoundError(f"Model directory not found: {model_dir}")

    models = {}
    for filename in os.listdir(model_dir):
        current_app.logger.debug(f"Processing file: {filename}")
        if filename.endswith('.h5'):
            model_id = os.path.splitext(filename)[0]
            model_path = os.path.join(model_dir, filename)
            data_path = f"{model_path}_data.pkl"

            current_app.logger.debug(f"Attempting to load model: {model_path}")
            current_app.logger.debug(f"Attempting to load data: {data_path}")

            try:
                # Use run_in_executor for potentially blocking I/O operations
                loop = asyncio.get_event_loop()
                model = await loop.run_in_executor(None, lambda: custom_load_model(model_path))
                
                with open(data_path, 'rb') as f:
                    network_input, pitchnames, note_to_int, n_vocab = pickle.load(f)
                
                models[model_id] = (model, network_input, pitchnames, note_to_int, n_vocab)
                current_app.logger.info(f"Successfully loaded model and data: {model_id}")
            except Exception as e:
                current_app.logger.error(f"Error loading model {model_id}: {str(e)}")
                current_app.logger.error(f"Traceback: {traceback.format_exc()}")

    current_app.logger.debug(f"Returning models: {list(models.keys())}")
    return models


async def generate_melody(model_id):
    """
    Generate a new melody using the specified model.

    This function uses the provided model ID to generate a new melody,
    converts it to MIDI format, and saves it to a file.

    Args:
        model_id (str): The ID of the model to use for generation.

    Returns:
        str: The path to the generated melody file.

    Raises:
        ValueError: If the specified model_id is not found.
        Exception: If there's an error during melody generation or saving.
    """
    current_app.logger.debug(f"Entering generate_melody function with model_id: {model_id}")

    models = await get_available_models()
    if model_id not in models:
        current_app.logger.error(f"Invalid model ID: {model_id}")
        raise ValueError(f"Invalid model ID: {model_id}")

    model, network_input, pitchnames, note_to_int, n_vocab = models[model_id]

    current_app.logger.debug(f"Model loaded. n_vocab: {n_vocab}, type: {type(n_vocab)}")
    current_app.logger.debug(f"network_input shape: {network_input.shape}")
    current_app.logger.debug(f"Number of unique pitches: {len(pitchnames)}")

    n_vocab = len(pitchnames)  # Ensure n_vocab is an integer
    current_app.logger.debug(f"Using n_vocab: {n_vocab}")

    current_app.logger.debug("Generating notes for the melody")
    generated_notes = await _generate_notes(model, network_input, pitchnames, note_to_int, n_vocab)

    current_app.logger.debug("Converting notes to MIDI")
    if 'OUTPUT_DIR' not in current_app.config:
        current_app.logger.error("OUTPUT_DIR not found in app config")
        raise ValueError("OUTPUT_DIR configuration is missing")

    output_dir = current_app.config['OUTPUT_DIR']
    if not os.path.exists(output_dir):
        current_app.logger.warning(f"Output directory does not exist, creating: {output_dir}")
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"generated_melody_{int(time.time())}.mid")
    current_app.logger.debug(f"Saving MIDI to file: {output_file}")
    await _create_midi(generated_notes, output_file)

    current_app.logger.debug(f"Melody generation complete. File saved: {output_file}")
    return output_file

async def _generate_notes(model, network_input, pitchnames, n_vocab, num_notes=500, temperature=1.0):
    """
    Generate a sequence of notes using the provided model.

    This internal function uses the trained model to generate a sequence
    of notes for the melody.

    Args:
        model: The trained Keras model.
        network_input: The input data used to train the model.
        pitchnames: A list of all unique pitches in the training data.
        note_to_int: A dictionary mapping note strings to integers.
        n_vocab: The number of unique pitches.
        sequence_length: The length of input sequences for the model.
        num_notes: The number of notes to generate.

    Returns:
        A list of generated notes and chords.
    """
    # Start with a random sequence from the input data
    current_app.logger.debug(f"Entering _generate_notes. n_vocab: {n_vocab}")
    start = np.random.randint(0, len(network_input) - 1)
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    pattern = network_input[start]
    prediction_output = []

    for _ in range(num_notes):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)
        
        prediction = model.predict(prediction_input, verbose=0)
        
        # Apply temperature scaling
        prediction = np.log(prediction) / temperature
        exp_preds = np.exp(prediction)
        prediction = exp_preds / np.sum(exp_preds)
        
        index = np.random.choice(range(len(prediction[0])), p=prediction[0])
        result = int_to_note[index]
        prediction_output.append(result)
        
        pattern = np.append(pattern, index)
        pattern = pattern[1:]
    
    current_app.logger.debug(f"Notes generated. Length: {len(prediction_output)}")
    return prediction_output

async def _create_midi(prediction_output, filename="generated_melody.mid"):
    """
    Create a MIDI file from the generated notes.

    This internal function takes the generated notes and converts them
    into a MIDI file, which is then saved to disk.

    Args:
        prediction_output: A list of generated notes and chords.
        filename: The name of the file to save the MIDI to.

    Returns:
        None
    """
    offset = 0
    output_notes = []

    # Create note and chord objects
    for pattern in prediction_output:
        # If the pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # If it's a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # Increase offset for next note
        offset += 0.5

    # Create the MIDI stream
    midi_stream = stream.Stream(output_notes)

    # Write the MIDI file
    midi_stream.write('midi', fp=filename)
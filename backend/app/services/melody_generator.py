import os
import time
import pickle
import numpy as np
from flask import current_app
from tensorflow.keras.models import load_model
from music21 import instrument, note, stream, chord

def get_available_models():
    """
    Retrieve and load available melody generation models.

    This function scans the MODEL_DIR for .h5 files (Keras models) and
    their corresponding .pkl files (containing model data). It loads
    these models and their associated data into memory.

    Returns:
        A dictionary where keys are model IDs and values are tuples
        containing the loaded model and its associated data.

    Raises:
        Exception: If there's an error loading a model or its data.
    """
    models = {}
    model_dir = current_app.config['MODEL_DIR']

    for filename in os.listdir(model_dir):
        if filename.endswith('.h5'):
            model_id = os.path.splitext(filename)[0]
            model_path = os.path.join(model_dir, filename)
            data_path = f"{model_path}_data.pkl"

            try:
                model = load_model(model_path)
                with open(data_path, 'rb') as f:
                    network_input, pitchnames, note_to_int, n_vocab = pickle.load(f)
                models[model_id] = (model, network_input, pitchnames, note_to_int, n_vocab)
                current_app.logger.info(f"Successfully loaded model and data: {model_id}")
            except Exception as e:
                current_app.logger.error(f"Error loading model {model_id}: {str(e)}")

    return models

def generate_melody(model_id):
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
    models = get_available_models()
    if model_id not in models:
        raise ValueError(f"Invalid model ID: {model_id}")

    model, network_input, pitchnames, note_to_int, n_vocab = models[model_id]

    # Generate notes for the melody
    generated_notes = _generate_notes(model, network_input, pitchnames, note_to_int, n_vocab)

    # Convert notes to MIDI and save to file
    output_file = os.path.join(current_app.config['OUTPUT_DIR'], f"generated_melody_{int(time.time())}.mid")
    _create_midi(generated_notes, output_file)

    return output_file

def _generate_notes(model, network_input, pitchnames, note_to_int, n_vocab, sequence_length=100, num_notes=500):
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
    start = np.random.randint(0, len(network_input) - 1)
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    pattern = network_input[start]
    prediction_output = []

    # Generate notes
    for _ in range(num_notes):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern = np.append(pattern, index)
        pattern = pattern[1:]

    return prediction_output

def _create_midi(prediction_output, filename="generated_melody.mid"):
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
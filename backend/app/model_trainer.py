import os
import numpy as np
import tensorflow as tf
from music21 import converter, note, chord
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import pickle

import tensorflow as tf

# Configure TensorFlow to use the GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs", flush=True)
    except RuntimeError as e:
        print(e)

def prepare_sequences(notes, sequence_length=100):
    if not notes:
        raise ValueError("The notes list is empty. No data to process.")
    
    pitchnames = sorted(set(item for item in notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    
    network_input = []
    network_output = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])
    
    if not network_input or not network_output:
        raise ValueError("No sequences could be prepared. Check if the input data is sufficient.")
    
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(len(pitchnames))
    network_output = to_categorical(network_output)
    
    return network_input, network_output, pitchnames, note_to_int

def create_model(network_input, n_vocab):
    model = Sequential()
    model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(256))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    return model

def train_model(model, network_input, network_output, epochs=50, batch_size=64):
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath, monitor='loss', 
        verbose=0,        
        save_best_only=True,        
        mode='min'
    )    
    callbacks_list = [checkpoint]     
    model.fit(network_input, network_output, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)

def prepare_data(midi_directory):
    print(f"Looking for MIDI files in: {midi_directory}", flush=True)
    midi_files = [f for f in os.listdir(midi_directory) if f.endswith(".mid")]
    print(f"Found {len(midi_files)} MIDI files: {midi_files}", flush=True)

    if not midi_files:
        raise ValueError("No MIDI files found. Please add some MIDI files to the midi_files directory.")

    notes = []
    for file in midi_files:
        midi_path = os.path.join(midi_directory, file)
        print(f"Processing file: {midi_path}", flush=True)
        try:
            midi = converter.parse(midi_path)
            notes_to_parse = midi.flat.notes
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Error processing {file}: {str(e)}", flush=True)

    print(f"Total notes extracted: {len(notes)}", flush=True)

    if not notes:
        raise ValueError("No notes were extracted from the MIDI files. Please check if the MIDI files are valid.")

    return notes

def load_or_train_model(midi_directory, model_path):
    print(f"Debug: Entering load_or_train_model function", flush=True)
    print(f"Debug: model_path = {model_path}", flush=True)
    print(f"Debug: midi_directory = {midi_directory}", flush=True)

    data_path = f"{model_path}_data.pkl"
    
    if os.path.exists(model_path) and os.path.exists(data_path):
        print(f"Debug: Existing model and data found", flush=True)
        model = load_model(model_path)
        print(f"Debug: Model loaded successfully", flush=True)
        
        with open(data_path, "rb") as f:
            network_input, pitchnames, note_to_int, n_vocab = pickle.load(f)
        print(f"Debug: Preprocessed data loaded successfully", flush=True)
    else:
        print(f"Debug: Model or preprocessed data not found", flush=True)
        print(f"Debug: Preparing data and training a new model", flush=True)
        notes = prepare_data(midi_directory)
        network_input, network_output, pitchnames, note_to_int = prepare_sequences(notes)
        n_vocab = len(set(notes))

        model = create_model(network_input, n_vocab)
        train_model(model, network_input, network_output)
        model.save(model_path)
        print(f"Debug: Model saved as {model_path}", flush=True)

        print(f"Debug: Saving preprocessed data to {data_path}", flush=True)
        with open(data_path, "wb") as f:
            pickle.dump((network_input, pitchnames, note_to_int, n_vocab), f)

    print(f"Debug: Exiting load_or_train_model function", flush=True)
    return model, network_input, pitchnames, note_to_int, n_vocab
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

print("Starting script...")

try:
    print("Importing os...")
    import os
    print("os imported successfully")

    print("Importing numpy...")
    import numpy as np
    print("numpy imported successfully")

    print("Importing tensorflow...")
    import tensorflow as tf
    print(f"TensorFlow version: {tf.__version__}")
    print("TensorFlow imported successfully")

    print("Importing music21...")
    from music21 import converter, note, chord
    print("music21 imported successfully")

    print("Importing keras modules...")
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.utils import to_categorical
    print("keras modules imported successfully")

    print("Importing pickle...")
    import pickle
    print("pickle imported successfully")

    print("Importing inquirer...")
    import inquirer
    print("inquirer imported successfully")

except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error during imports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("All imports successful")

# Configure TensorFlow to use the GPU
print("Configuring TensorFlow for GPU usage...")
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs", flush=True)
    except RuntimeError as e:
        print(f"RuntimeError during GPU configuration: {e}")
else:
    print("No GPUs found. Will use CPU.")

def prepare_sequences(notes, sequence_length=100):
    print(f"Preparing sequences with {len(notes)} notes...")
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
    
    print(f"Sequences prepared. Input shape: {network_input.shape}, Output shape: {network_output.shape}")
    return network_input, network_output, pitchnames, note_to_int

def create_model(network_input, n_vocab):
    print(f"Creating model with input shape {network_input.shape} and {n_vocab} vocabulary size...")
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
    print("Model created successfully")
    return model

def train_model(model, network_input, network_output, epochs=50, batch_size=64):
    print(f"Training model with {epochs} epochs and batch size {batch_size}...")
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath, monitor='loss', 
        verbose=1,        
        save_best_only=True,        
        mode='min'
    )    
    callbacks_list = [checkpoint]     
    history = model.fit(network_input, network_output, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)
    print(f"Model training completed. Final loss: {history.history['loss'][-1]}")

def prepare_data(midi_directory):
    print(f"Preparing data from directory: {midi_directory}")
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

def select_directory(base_path, prompt):
    print(f"Selecting directory from {base_path}")
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not directories:
        print(f"No directories found in {base_path}", flush=True)
        return None
    
    print(f"{prompt}")
    for i, directory in enumerate(directories):
        print(f"{i+1}. {directory}")
    
    while True:
        try:
            choice = input("Enter the number of your choice: ")
            index = int(choice) - 1
            if 0 <= index < len(directories):
                selected = os.path.join(base_path, directories[index])
                print(f"Selected directory: {selected}")
                return selected
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def load_or_train_model(midi_directory, model_path):
    print(f"Entering load_or_train_model function")
    print(f"model_path = {model_path}")
    print(f"midi_directory = {midi_directory}")

    model_dir = os.path.dirname(model_path)
    os.makedirs(model_dir, exist_ok=True)  # Ensure model directory exists

    data_path = f"{model_path}_data.pkl"
    
    if os.path.exists(model_path) and os.path.exists(data_path):
        print(f"Existing model and data found")
        model = load_model(model_path)
        print(f"Model loaded successfully")
        
        with open(data_path, "rb") as f:
            network_input, pitchnames, note_to_int, n_vocab = pickle.load(f)
        print(f"Preprocessed data loaded successfully")
    else:
        print(f"Model or preprocessed data not found")
        print(f"Preparing data and training a new model")
        notes = prepare_data(midi_directory)
        network_input, network_output, pitchnames, note_to_int = prepare_sequences(notes)
        n_vocab = len(set(notes))

        model = create_model(network_input, n_vocab)
        train_model(model, network_input, network_output)
        model.save(model_path)
        print(f"Model saved as {model_path}")

        print(f"Saving preprocessed data to {data_path}")
        with open(data_path, "wb") as f:
            pickle.dump((network_input, pitchnames, note_to_int, n_vocab), f)

    print(f"Exiting load_or_train_model function")
    return model, network_input, pitchnames, note_to_int, n_vocab

def main():
    print("Entering main function")
    try:
        input_base = "/app/input"
        model_base = "/app/model"
        
        print("About to select input directory")
        input_dir = select_directory(input_base, "Select the input directory containing MIDI files:")
        if not input_dir:
            print("No input directory selected. Exiting.")
            return

        # We'll use a fixed path for the model output
        model_path = os.path.join(model_base, "trained_model.h5")
        
        # Ensure the model directory exists
        os.makedirs(model_base, exist_ok=True)
        
        print(f"Model will be saved to: {model_path}")
        
        model, network_input, pitchnames, note_to_int, n_vocab = load_or_train_model(input_dir, model_path)
        
        print("Model training/loading complete.")
    except Exception as e:
        print(f"Error in main function: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Script execution started")
    main()
    print("Script execution completed")
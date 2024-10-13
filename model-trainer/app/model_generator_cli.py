# MIDI Music Generation Model Training Script
# This script processes MIDI files, trains a neural network model, and prepares for music generation.
# It uses TensorFlow, Keras, and music21 libraries for deep learning and music processing.

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

print("Starting script...")

try:
    # Import necessary libraries
    print("Importing os...")
    import os
    print("os imported successfully")

    print("Importing numpy...")
    import numpy as np
    print("numpy imported successfully")

    print("Importing tensorflow...")
    import tensorflow as tf
    print(f"TensorFlow version: {tf.__version__}")
    print(tf.test.is_built_with_cuda())
    print(tf.config.list_physical_devices('GPU'))
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
    # Handle import errors
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    # Handle unexpected errors during import
    print(f"Unexpected error during imports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("All imports successful")

# Configure TensorFlow to use the GPU if available
print("Configuring TensorFlow for GPU usage...")
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Configure GPU memory growth
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs", flush=True)
    except RuntimeError as e:
        print(f"RuntimeError during GPU configuration: {e}")
else:
    print("No GPUs found. Will use CPU.")

def prepare_sequences(notes, sequence_length=100):
    """
    Prepare input sequences for the neural network.

    Args:
    notes (list): List of musical notes and chords.
    sequence_length (int): Length of each input sequence.

    Returns:
    tuple: Processed network input, output, pitch names, and note-to-integer mapping.
    """
    print(f"Preparing sequences with {len(notes)} notes...")
    if not notes:
        raise ValueError("The notes list is empty. No data to process.")
    
    # Create a set of unique pitch names
    pitchnames = sorted(set(item for item in notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    
    network_input = []
    network_output = []
    # Create input sequences and corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])
    
    if not network_input or not network_output:
        raise ValueError("No sequences could be prepared. Check if the input data is sufficient.")
    
    # Reshape and normalise input
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(len(pitchnames))
    network_output = to_categorical(network_output)
    
    print(f"Sequences prepared. Input shape: {network_input.shape}, Output shape: {network_output.shape}")
    return network_input, network_output, pitchnames, note_to_int

def create_model(network_input, n_vocab):
    """
    Create and compile the LSTM neural network model.

    Args:
    network_input (numpy.ndarray): Processed input sequences.
    n_vocab (int): Size of the vocabulary (number of unique notes/chords).

    Returns:
    keras.models.Sequential: Compiled Keras model.
    """
    print(f"Creating model with input shape {network_input.shape} and {n_vocab} vocabulary size...")
    # Create a Sequential model
    # This is a linear stack of layers where we can add layers one by one
    model = Sequential()

    # Add the first LSTM layer
    model.add(LSTM(
        256,  # Number of LSTM units (dimensionality of the output space)
        input_shape=(network_input.shape[1], network_input.shape[2]),  # Shape of input data (sequence length, features)
        return_sequences=True  # Whether to return the last output or the full sequence
    ))
    # This layer processes the input sequence and returns sequences of 256-dimensional vectors

    # Add a Dropout layer for regularisation
    model.add(Dropout(0.3))
    # This randomly sets 30% of the inputs to 0 during training, which helps prevent overfitting

    # Add a second LSTM layer
    model.add(LSTM(
        512,  # Increase the number of LSTM units to 512
        return_sequences=True  # Still return sequences as we have another LSTM layer coming
    ))
    # This layer processes the sequences from the previous layer, creating more complex representations

    # Another Dropout layer
    model.add(Dropout(0.3))
    # Again, this helps prevent overfitting

    # Add a third LSTM layer
    model.add(LSTM(256))  # Note: no return_sequences=True here
    # This final LSTM layer returns only the last output, not the full sequence

    # Add a Dense (fully connected) layer
    model.add(Dense(256))
    # This layer performs a linear transformation on the 256-dimensional input

    # Another Dropout layer
    model.add(Dropout(0.3))
    # One more layer of regularisation to prevent overfitting

    # Add the output layer
    model.add(Dense(
        n_vocab,  # Number of units equals the vocabulary size (number of possible output notes/chords)
        activation='softmax'  # Softmax activation for multi-class classification
    ))
    # This layer outputs probabilities for each possible note/chord in the vocabulary

    # Compile the model
    model.compile(
        loss='categorical_crossentropy',  # Loss function suitable for multi-class classification
        optimizer='rmsprop'  # RMSprop optimizer, generally good for recurrent neural networks
    )
    # This sets up the model for training, defining how it will measure its error (loss function)
    # and how it will adjust its weights (optimizer)
    print("Model created successfully")
    return model

def train_model(model, network_input, network_output, epochs=50, batch_size=64):
    """
    Train the neural network model.

    Args:
    model (keras.models.Sequential): The model to train.
    network_input (numpy.ndarray): Input data for training.
    network_output (numpy.ndarray): Target output data for training.
    epochs (int): Number of training epochs.
    batch_size (int): Batch size for training.

    Returns:
    None
    """
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
    """
    Process MIDI files and extract notes and chords.

    Args:
    midi_directory (str): Path to the directory containing MIDI files.

    Returns:
    list: Extracted notes and chords from all MIDI files.
    """
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
    """
    Prompt the user to select a directory from a list.

    Args:
    base_path (str): The base path containing directories to choose from.
    prompt (str): The prompt message for the user.

    Returns:
    str: The selected directory path, or None if no selection was made.
    """
    print(f"Selecting directory from {base_path}")
    print(f"Directory contents: {os.listdir(base_path)}")
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
    """
    Load an existing model or train a new one if it doesn't exist.

    Args:
    midi_directory (str): Path to the directory containing MIDI files.
    model_path (str): Path where the model should be saved or loaded from.

    Returns:
    tuple: The model, network input, pitch names, note-to-integer mapping, and vocabulary size.
    """
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
    """
    Main function to orchestrate the model training process.
    """
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
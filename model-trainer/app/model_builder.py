# model_builder.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class ModelBuilder:
    """
    A class for building the neural network model.

    This class provides a method to create a Sequential model with LSTM layers
    for music generation.
    """

    def create_model(self, network_input, n_vocab):
        """
        Create and compile the LSTM neural network model.

        This method builds a Sequential model with multiple LSTM layers and
        Dense layers, designed for music generation.

        Args:
            network_input (numpy.ndarray): Processed input sequences.
            n_vocab (int): Size of the vocabulary (number of unique notes/chords).

        Returns:
            keras.models.Sequential: Compiled Keras model.
        """
        print(f"Creating model with input shape {network_input.shape} and {n_vocab} vocabulary size...")
        
        # Create a Sequential model
        model = Sequential()

        # First LSTM layer
        model.add(LSTM(
            512,  # Number of LSTM units
            input_shape=(network_input.shape[1], network_input.shape[2]),
            return_sequences=True  # Return full sequence
        ))
        # This layer processes the input sequence and returns sequences of 512-dimensional vectors

        # Dropout layer for regularisation
        model.add(Dropout(0.3))
        # This randomly sets 30% of the inputs to 0 during training, which helps prevent overfitting

        # Second LSTM layer
        model.add(LSTM(
            512,  # Number of LSTM units
            return_sequences=True
        ))
        # This layer processes the sequences from the previous layer, creating more complex representations

        # Another Dropout layer
        model.add(Dropout(0.3))

        # Third LSTM layer
        model.add(LSTM(512))  # No return_sequences=True here
       # This layer processes the sequences from the previous layer, creating more complex representations

        # Dense layer
        model.add(Dense(256))
        # This layer performs a linear transformation on the 256-dimensional input

        # Another Dropout layer
        model.add(Dropout(0.3))

        # Output layer
        model.add(Dense(
            n_vocab,
            activation='softmax'  # Softmax activation for multi-class classification
        ))
        # This layer outputs probabilities for each possible note/chord in the vocabulary

        # Compile the model
        model.compile(
            loss='categorical_crossentropy',  # Loss function suitable for multi-class classification
            optimizer='adam'  # Adam optimiser for training
        )

        print("Model created successfully")
        return model
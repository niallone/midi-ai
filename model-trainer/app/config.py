import os

class Config:
    """
    Configuration class for the model trainer.

    This class holds all the configuration parameters for the model training process.
    It uses class attributes for simplicity, but could be extended to load from
    environment variables or a configuration file if needed.
    """

    # Base directory for input MIDI files
    INPUT_BASE = "/app/input"

    # Base directory for saving trained models
    MODEL_BASE = "/app/model"

    # Number of training epochs
    EPOCHS = 50

    # Batch size for training
    BATCH_SIZE = 64

    # Length of input sequences
    SEQUENCE_LENGTH = 100

def load_config():
    """
    Load and return the configuration.

    This function could be extended to load configuration from environment
    variables or a file. Currently, it simply returns an instance of the Config class.

    Returns:
        Config: An instance of the Config class.
    """
    return Config()
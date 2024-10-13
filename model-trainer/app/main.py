import os
import asyncio
from config import load_config
from midi_processor import MIDIProcessor
from model_builder import ModelBuilder
from model_trainer import ModelTrainer
from utils import setup_gpu, select_directory

async def main():
    """
    The main function that orchestrates the entire model training process.

    This asynchronous function performs the following steps:
    1. Loads the configuration
    2. Sets up the GPU for TensorFlow
    3. Prompts the user to select an input directory
    4. Processes MIDI files and prepares sequences
    5. Builds and trains the model
    6. Saves the trained model

    The function uses asyncio for potential future asynchronous operations,
    although the current implementation is mostly synchronous.
    """
    # Load the configuration settings
    config = load_config()

    # Set up the GPU for TensorFlow
    setup_gpu()

    # Prompt the user to select an input directory containing MIDI files
    input_dir = select_directory(config.INPUT_BASE, "Select the input directory containing MIDI files:")
    if not input_dir:
        print("No input directory selected. Exiting.")
        return

    # Define the path where the trained model will be saved
    model_path = os.path.join(config.MODEL_BASE, "trained_model.h5")
    # Ensure the model directory exists
    os.makedirs(config.MODEL_BASE, exist_ok=True)

    # Create an instance of the MIDIProcessor
    midi_processor = MIDIProcessor()

    # Process MIDI files and extract notes
    print("Processing MIDI files...")
    notes = midi_processor.prepare_data(input_dir)
    
    # Prepare sequences for model input
    print("Preparing sequences...")
    network_input, network_output, pitchnames, note_to_int = midi_processor.prepare_sequences(notes, config.SEQUENCE_LENGTH)
    n_vocab = len(set(notes))

    # Create an instance of the ModelBuilder and build the model
    print("Building the model...")
    model_builder = ModelBuilder()
    model = model_builder.create_model(network_input, n_vocab)

    # Create an instance of the ModelTrainer and train the model
    print("Training the model...")
    trainer = ModelTrainer(model)
    await trainer.train(network_input, network_output, model_path, config.EPOCHS, config.BATCH_SIZE)

    print("Model training complete.")

if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
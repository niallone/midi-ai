import tensorflow as tf

class ModelTrainer:
    """
    A class for training the neural network model.

    This class provides methods to train the model and save it to a file.
    """

    def __init__(self, model):
        """
        Initialise the ModelTrainer.

        Args:
            model (keras.models.Sequential): The model to be trained.
        """
        self.model = model

    async def train(self, network_input, network_output, model_path, epochs=50, batch_size=64):
        """
        Train the neural network model.

        This method trains the model using the provided input and output data,
        and saves the trained model to a file.

        Args:
            network_input (numpy.ndarray): Input data for training.
            network_output (numpy.ndarray): Target output data for training.
            model_path (str): Path where the trained model should be saved.
            epochs (int): Number of training epochs.
            batch_size (int): Batch size for training.

        Returns:
            None
        """
        print(f"Training model with {epochs} epochs and batch size {batch_size}...")
        
        # Define a callback to save the model during training
        filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath, monitor='loss', 
            verbose=1,        
            save_best_only=True,        
            mode='min'
        )    
        callbacks_list = [checkpoint]

        # Train the model
        history = self.model.fit(
            network_input, 
            network_output, 
            epochs=epochs, 
            batch_size=batch_size, 
            callbacks=callbacks_list
        )

        print(f"Model training completed. Final loss: {history.history['loss'][-1]}")

        # Save the trained model
        self.model.save(model_path)
        print(f"Model saved to {model_path}")
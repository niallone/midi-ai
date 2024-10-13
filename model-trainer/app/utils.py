import tensorflow as tf
import os

def setup_gpu():
    """
    Configure TensorFlow to use the GPU if available.

    This function attempts to configure TensorFlow to use GPU acceleration.
    If a GPU is available, it sets up memory growth to avoid allocating all GPU memory at once.
    """
    print("Configuring TensorFlow for GPU usage...")
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Configure GPU memory growth
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(f"{len(gpus)} Physical GPUs, {len(logical_gpus)} Logical GPUs")
        except RuntimeError as e:
            print(f"RuntimeError during GPU configuration: {e}")
    else:
        print("No GPUs found. Will use CPU.")

def select_directory(base_path, prompt):
    """
    Prompt the user to select a directory from a list.

    This function lists all directories in the given base path and asks the user
    to select one of them.

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
        print(f"No directories found in {base_path}")
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
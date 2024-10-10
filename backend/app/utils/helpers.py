import os

def ensure_directory_exists(directory):
    """
    Ensure that a directory exists, creating it if necessary.

    This helper function checks if a given directory exists, and creates
    it if it doesn't. This is useful for ensuring that output directories
    are available before trying to write files to them.

    Args:
        directory (str): The path of the directory to check/create.

    Returns:
        bool: True if the directory exists or was created successfully, 
              False otherwise.

    Raises:
        OSError: If there's an error creating the directory.
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except OSError as e:
        print(f"Error creating directory {directory}: {e}")
        return False

# Add more helper functions as needed
# For example:
# def validate_midi_file(file_path):
#     """
#     Validate that a file is a proper MIDI file.
#     """
#     # Implementation here

# def generate_unique_filename(base_name, extension):
#     """
#     Generate a unique filename to avoid overwriting existing files.
#     """
#     # Implementation here
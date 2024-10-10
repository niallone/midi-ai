import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the application.

    This class uses environment variables to configure the application.
    If an environment variable is not set, it falls back to a default value.
    """

    # Secret key for signing cookies and other security-related tasks
    # In production, this should be set to a complex, random value
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Directory for input MIDI files
    MIDI_DIR = os.environ.get('MIDI_DIR') or '/app/input'

    # Directory for output generated melodies
    OUTPUT_DIR = os.environ.get('OUTPUT_DIR') or '/app/output'

    # Directory for ML models
    MODEL_DIR = os.environ.get('MODEL_DIR') or '/app/model'

    # Database URI for SQLAlchemy
    # Falls back to a SQLite database if not set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

    # Disable SQLAlchemy modification tracking for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add more configuration options as needed
    # For example:
    # DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    # LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'INFO'
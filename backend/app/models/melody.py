from app.db.database import db
from datetime import datetime

class Melody(db.Model):
    """
    Melody model for storing information about generated melodies.

    This model represents a generated melody in the database. It stores
    information such as the filename, the model used to generate it,
    and the creation timestamp.

    Attributes:
        id (int): The primary key of the melody.
        filename (str): The filename of the generated MIDI file.
        model_id (str): The ID of the model used to generate the melody.
        created_at (datetime): The timestamp when the melody was generated.
    """

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    model_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Provide a string representation of the Melody instance.

        Returns:
            str: A string representation of the Melody.
        """
        return f'<Melody {self.filename} (Model: {self.model_id})>'

    def to_dict(self):
        """
        Convert the Melody instance to a dictionary.

        This method is useful for serializing the Melody object to JSON
        for API responses.

        Returns:
            dict: A dictionary representation of the Melody.
        """
        return {
            'id': self.id,
            'filename': self.filename,
            'model_id': self.model_id,
            'created_at': self.created_at.isoformat()
        }
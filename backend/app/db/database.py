from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

def init_db(app):
    """
    Initialise the database connection for the application.

    This function sets up the SQLAlchemy database connection using the
    application's configuration. It also creates all database tables
    if they do not already exist.

    Args:
        app: The Flask application instance.

    Returns:
        None
    """
    # Bind the database to the application
    db.init_app(app)

    # Create all tables in the database
    # This is equivalent to "Create Table" statements in raw SQL
    with app.app_context():
        db.create_all()

    # Add any additional database initialisation here
    # For example, creating initial records, setting up indexes, etc.
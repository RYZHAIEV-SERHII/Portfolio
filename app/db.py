from flask_sqlalchemy import SQLAlchemy

from src.db.models import metadata

# Initialize SQLAlchemy
database = SQLAlchemy(metadata=metadata)


def init_db(app):
    """
    Initialize the database with the Flask app.

    :param app: Flask application instance
    """
    database.init_app(app)

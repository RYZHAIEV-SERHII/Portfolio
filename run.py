import logging.config
import os

from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError

from app import create_app
from app.models import db

app = create_app()

# Initialize Flask-Migrate for handling migrations
migrate = Migrate(app, db)


# Load logging configuration from logging.conf
def setup_logging():
    # Ensure the 'logs/' directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.config.fileConfig("logging.conf")
    print("Logging enabled.")


# Function to check if the database connection is successful
def check_database_connection():
    try:
        with app.app_context():
            db.engine.execute("SELECT 1")  # A lightweight query to test connection
            print("Database connected successfully.")
    except OperationalError as e:
        error_message = "Error during connecting to the database."
        print(error_message)
        print(f"Details: {str(e)}")


if __name__ == "__main__":
    setup_logging()
    check_database_connection()
    app.run(host="0.0.0.0", port=5000)


# Optional features to show my skills.
# When it comes to deploying:
# TODO: Deploy application on a robust production server like Gunicorn or uWSGI
# TODO: Setup a web server Nginx.

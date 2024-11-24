import logging.config
import os

from sqlalchemy.exc import OperationalError

from api import create_api
from app import create_app
from app.db import database
from cli import cli as run_cli

app = create_app()
api = create_api()


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
            database.engine.connect()
            print("Database connected successfully.")
    except OperationalError as e:
        error_message = "Error during connecting to the database."
        print(error_message)
        print(f"Details: {str(e)}")


if __name__ == "__main__":
    setup_logging()
    check_database_connection()
    run_cli()

# Optional features to show my skills.
# When it comes to deploying:
# TODO: Deploy application on a robust production server like Gunicorn or uWSGI

# In production, it's better to run Flask with a WSGI server like gunicorn or uWSGI
# instead of using Flask’s built-in development server, which isn’t optimized for performance and scalability.
# Example:
# gunicorn -w 4 -b 0.0.0.0:5000 run:app

# TODO: Setup a web server Nginx.

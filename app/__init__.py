import os

from dotenv import load_dotenv
from flask import Flask

from config import env_config
from .db import init_db  # Import init_db function
from .mail import mail

load_dotenv()


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Dynamically load environment config
    env = os.getenv("FLASK_ENV", "development")  # Default to 'development'
    app.config.from_object(env_config[env])

    # Initialize the database with the app
    init_db(app)  # Use init_db function to initialize the database

    # Initialize the mail extension
    mail.init_app(app)

    # Import and register routes
    from .views import main

    app.register_blueprint(main)

    return app

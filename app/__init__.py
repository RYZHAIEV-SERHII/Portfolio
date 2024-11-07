import os

from dotenv import load_dotenv
from flask import Flask

from config import env_config
from .mail import mail
from .models import db

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Dynamically load environment config
    env = os.getenv("FLASK_ENV", "development")  # Default to 'development'
    app.config.from_object(env_config[env])

    # Initialize the database with the app
    db.init_app(app)

    # Initialize the mail extension
    mail.init_app(app)

    # Import and register routes
    from .views import main

    app.register_blueprint(main)

    return app

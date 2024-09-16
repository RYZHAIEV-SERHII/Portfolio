import os

from flask import Flask

from config import env_config


def create_app():
    app = Flask(__name__)

    # Dynamically load environment config
    env = os.getenv("FLASK_ENV", "development")  # Default to 'development'
    app.config.from_object(env_config[env])

    # Import and register routes
    from .views import main

    app.register_blueprint(main)

    return app

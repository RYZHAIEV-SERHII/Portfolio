import logging.config
import os

from app import create_app

app = create_app()


# Load logging configuration from logging.conf
def setup_logging():
    # Ensure the 'logs/' directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.config.fileConfig("logging.conf")


if __name__ == "__main__":
    setup_logging()
    app.run(host="0.0.0.0", port=5000)

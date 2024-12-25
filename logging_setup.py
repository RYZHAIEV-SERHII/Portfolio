import logging.config
import os


# Get the loggers
app_logger = logging.getLogger("appLogger")
api_logger = logging.getLogger("apiLogger")
cli_logger = logging.getLogger("cliLogger")


# Load logging configuration from logging.conf
def setup_logging():
    # Ensure the 'logs/' directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.config.fileConfig("logging.conf")

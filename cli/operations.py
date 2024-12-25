import subprocess

from logging_setup import app_logger, api_logger


def run_flask_app() -> None:
    """
    Run the Flask app using Gunicorn.

    This function starts the Flask app on port 5000 with 1 worker.
    Gunicorn is used as the WSGI HTTP server with the following options:
    - -w 1: Sets the number of worker processes to 1.
    - -b 0.0.0.0:5000: Binds the server to all network interfaces on port 5000.
    - --log-level info: Sets the logging level to 'info' for detailed output.
    - --reload: Enables automatic reloading of the server on code changes.
    """
    app_logger.info("Starting Flask app...")
    app_logger.info("App logging enabled.")

    subprocess.Popen(
        [
            "gunicorn",
            "-w",
            "1",
            "-b",
            "0.0.0.0:5000",
            "--log-level",
            "info",
            "--reload",
            "run:app",
        ]
    )
    app_logger.info("Flask app is running on http://localhost:5000")


def run_fast_api() -> None:
    """
    Run the FastAPI app using Gunicorn.

    This function starts the FastAPI app on port 8000 with 1 worker.
    Gunicorn is used as the WSGI HTTP server with Uvicorn as the worker class.

    Options used:
    - -k uvicorn.workers.UvicornWorker: Specifies the worker class to use, which is Uvicorn.
    - -w 1: Sets the number of worker processes to 1.
    - -b 0.0.0.0:8000: Binds the server to all network interfaces on port 8000.
    - --log-level info: Sets the logging level to 'info' for detailed output.
    - --reload: Enables automatic reloading of the server on code changes.
    """
    api_logger.info("Starting FastAPI app...")
    api_logger.info("API logging enabled.")

    subprocess.Popen(
        [
            "gunicorn",
            "-k",
            "uvicorn.workers.UvicornWorker",
            "-w",
            "1",
            "-b",
            "0.0.0.0:8000",
            "--log-level",
            "info",
            "--reload",
            "run:api",
        ]
    )
    api_logger.info("FastAPI app is running on http://localhost:8000")


def run_all() -> None:
    """
    Run both Flask and FastAPI apps.

    This function starts both the Flask and FastAPI apps concurrently.
    """
    run_flask_app()
    run_fast_api()


def stop_flask_app() -> None:
    """
    Stop the Flask app.

    This function stops the Flask app.
    """
    subprocess.run(["pkill", "-f", "gunicorn.*run:app"])
    app_logger.info("Flask app stopped.")


def stop_fast_api() -> None:
    """
    Stop the FastAPI app.

    This function stops the FastAPI app.
    """
    subprocess.run(["pkill", "-f", "gunicorn.*run:api"])
    api_logger.info("FastAPI app stopped.")


def stop_all() -> None:
    """
    Stop both Flask and FastAPI apps.

    This function stops both the Flask and FastAPI apps.
    """
    stop_flask_app()
    stop_fast_api()

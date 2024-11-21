import argparse
import os
from typing import Optional, Callable, Dict

from .operations import (
    run_flask_app,
    run_fast_api,
    run_all,
    stop_flask_app,
    stop_fast_api,
    stop_all,
)


def run_setup(command: str, service: str) -> None:
    """
    Run the specified setup based on the command provided.

    Args:
        command (str): The command to run. Expected values are "start" and "stop".
        service (str): The service to run. Expected values are "app", "api", and "all".
    """
    # Mapping of command strings to their corresponding setup functions
    setup_functions: Dict[str, Dict[str, Callable[[], None]]] = {
        "start": {
            "app": run_flask_app,
            "api": run_fast_api,
            "all": run_all,
        },
        "stop": {
            "app": stop_flask_app,
            "api": stop_fast_api,
            "all": stop_all,
        },
    }
    # Retrieve the setup function based on the command and service
    setup_function: Optional[Callable[[], None]] = setup_functions.get(command, {}).get(
        service
    )

    # Execute the setup function if found, otherwise print an error message
    if setup_function:
        setup_function()
    else:
        print(f"Unknown command or service: {command} {service}")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments to determine which setup to run.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run Flask and FastAPI apps",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="?",
        default=os.getenv("DEFAULT_COMMAND"),
        choices=["start", "stop"],
        help="Command to run",
    )
    parser.add_argument(
        "service",
        nargs="?",
        default=os.getenv("DEFAULT_SERVICE"),
        choices=["app", "api", "all"],
        help="Service to run",
    )
    return parser.parse_args()

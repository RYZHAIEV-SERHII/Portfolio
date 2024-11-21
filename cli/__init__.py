"""
Command-line interface for managing app setups.

This module provides a command-line interface for running different app setups.
The interface can be used to start either the Flask or FastAPI app, or both
concurrently.

The command-line interface accepts a single argument, "command", which
specifies which app setup to run. The available commands are "start" and "stop".
The available services are "app", "api", and "all".

Usage:
    python cli.py [command] [service]

Example:
    python3 cli.py start all
    python3 cli.py stop all
"""

from cli.setup import parse_arguments, run_setup


def cli() -> None:
    """
    Run the command-line interface for managing app setups.

    This function parses command-line arguments to determine which setup to run.

    Prints information about the setup to run and the command-line arguments
    used.
    """
    print("Starting CLI...")
    args = parse_arguments()
    print(f"Running setup: {args.command} {args.service}")
    run_setup(args.command, args.service)


if __name__ == "__main__":
    cli()

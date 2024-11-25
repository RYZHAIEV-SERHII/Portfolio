"""
This script is the entry point for the FastAPI application.
It imports the FastAPI object from api/__init__.py and starts
the development server if the script is run directly.
"""

from api import create_api

portfolio_api = create_api()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(portfolio_api, host="0.0.0.0", port=8000, log_level="info", reload=True)

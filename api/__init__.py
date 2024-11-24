import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from .db import init_db
from .routes import projects

from config import env_config

load_dotenv()


def create_api():
    """
    Create and configure the FastAPI application.
    """
    api: FastAPI = FastAPI()

    # Dynamically load environment config
    env = os.getenv("FAST_ENV", "development")  # Default to 'development'
    api_config = env_config[env]  # Get the configuration class

    # Set the configuration to the FastAPI state
    api.state.config = api_config

    # Initialize the database with the api
    init_db(api)  # Use init_db function to initialize the database

    # Create the API router
    api_router = APIRouter(prefix="/api")

    # Include routers
    api_router.include_router(projects.router)
    # api_router.include_router(skills.router)
    # api_router.include_router(experiences.router)
    # api_router.include_router(education.router)
    # api_router.include_router(resume.router)
    # api_router.include_router(contact.router)
    # api_router.include_router(about.router)

    # Include the API router
    api.include_router(api_router)

    return api

"""
Database setup and session management

This module contains functions for initializing the database, creating database sessions,
and providing a context manager for database sessions.

"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from src.db.models import metadata

load_dotenv()


class Database:
    """
    Database setup and session management

    This class provides functions for initializing the database,
    creating database sessions, and providing a context manager for database sessions.

    """

    def __init__(self):
        """
        Initialize the database engine and session maker.

        """
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def init_db(self):
        """
        Initialize the database.

        This function creates all tables in the database.

        """
        metadata.create_all(self.engine)

    def get_db_session(self):
        """
        Get a database session.

        This is a context manager that yields a database session.
        The session is closed at the end of the context.

        Yields:
            sqlalchemy.orm.Session: The database session

        """
        session = self.session()
        try:
            yield session
        finally:
            session.close()


# Make an instance of the Database class
database = Database()

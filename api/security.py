import os
from functools import wraps

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.db import database
from src.db.models import User

load_dotenv()

# Load environment variables from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Initialize the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash a plain password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


class AuthorizationError(HTTPException):
    """
    Custom exception for authorization errors.

    Attributes:
        status_code (int): HTTP status code for the error.
        detail (str): Error message.
        headers (dict, optional): Headers to include in the response.
    """

    def __init__(self, status_code: int, detail: str, headers=None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def check_authorization(
    resource_model,
    unauthorized_message: str = "Unauthorized to access this resource",
):
    """
    Decorator to check if the current user is authorized to access a resource.

    Args:
    - resource_model (type): The model type of the resource.
    - unauthorized_message (str): The unauthorized error message.

    Returns:
    - function: A decorator that checks if the current user is authorized to access the resource.
    """

    def decorator(func):
        """
        Decorator function to check if the current user is authorized to access a resource.
        """

        @wraps(func)
        async def wrapper(
            *args,
            db: Session = Depends(database.get_db_session),
            current_user: User = Depends(get_current_user),
            **kwargs,
        ):
            """
            Wrapper function that checks if the current user is authorized to access a resource.
            """
            # Retrieve the resource from the database
            resource_id = kwargs.get("id")
            if resource_id is None:
                raise HTTPException(status_code=400, detail="Resource ID not provided")

            resource = (
                db.query(resource_model)
                .filter(resource_model.id == resource_id)
                .first()
            )

            # Check if the user is authenticated
            if not current_user or not current_user.id:
                raise HTTPException(status_code=401, detail="Invalid user credentials")

            # Check if the resource exists
            if not resource:
                raise HTTPException(
                    status_code=404, detail=f"{resource_model.__name__} not found"
                )

            # Check if the current user is authorized
            if resource.user_id != current_user.id:
                raise HTTPException(status_code=403, detail=unauthorized_message)

            return await func(*args, **kwargs)

        return wrapper

    return decorator


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db_session)
) -> User:
    """
    Retrieve the current user from the provided token.

    Args:
        token (str): The OAuth2 access token.
        db (Session): The database session.

    Returns:
        User: The user instance associated with the token.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    # Define the exception to be raised for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token to extract the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract user ID from the token payload
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        # Raise an exception if there's an error decoding the token
        raise credentials_exception

    # Query the database to find the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        # Raise an exception if the user does not exist
        raise credentials_exception

    # Return the user instance if found
    return user


def create_access_token(data: dict) -> str:
    """
    Create a new JWT access token.

    Args:
        data (dict): The payload data to encode in the JWT.

    Returns:
        str: The encoded JWT token.
    """
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

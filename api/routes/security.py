"""
API endpoints for authentication
"""

from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.db import database
from api.security import verify_password, AuthorizationError, create_access_token
from src.db.models import User

# Create FastAPI router for authentication endpoints
router = APIRouter(tags=["Authentication"])


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db_session),
):
    """
    Generate a new access token for a user.

    This endpoint takes an OAuth2 password request form and verifies the user's
    credentials. If the credentials are valid, the endpoint returns a new access
    token.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise AuthorizationError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire = timedelta(minutes=30)
    now = datetime.now(timezone.utc)
    token_data = {"sub": str(user.id), "exp": now + expire}
    access_token = create_access_token(token_data)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expire.total_seconds(),
    }

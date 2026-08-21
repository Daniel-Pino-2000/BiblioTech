"""Login and "who am I" endpoints. Registration lives in routers/users.py
(POST /users) since a new user is a resource being created, not an auth
action -- only issuing/reading a token belongs here."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserResponse
from app.services import users_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2-compatible token login. Accepts form data (username, password)
    and returns a JWT bearer token used to authenticate subsequent requests.
    """
    user = users_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Return the profile of whoever the bearer token belongs to.

    Used by the frontend on load to restore a session from a stored token."""
    return current_user

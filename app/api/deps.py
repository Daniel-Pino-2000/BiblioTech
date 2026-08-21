"""
Shared FastAPI dependencies: a DB session per request, and the two auth
guards (`get_current_user`, `get_current_admin_user`) every protected router
imports from here rather than reimplementing.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import SessionLocal
from app.models.user import User
from app.services import users_service


def get_db():
    """Yield a request-scoped SQLAlchemy session, closed once the request finishes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the bearer token on the request into a User row.

    Used as `current_user: User = Depends(get_current_user)` on any endpoint
    that requires *some* logged-in user; endpoints that also need to check
    ownership (e.g. "is this your cart?") compare current_user.id themselves.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = users_service.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Same as get_current_user, plus a 403 if the account isn't an admin.

    Used on catalog-mutating routes (create-book, discount, create-author).
    There's no HTTP way to grant admin -- see scripts/make_admin.py."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user

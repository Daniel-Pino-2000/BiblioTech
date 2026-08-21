"""
Password hashing and JWT issuing/verification. Nothing here talks to the
database or FastAPI directly -- it's pure crypto/token logic, which keeps it
easy to unit test and reuse from both the auth router and app.api.deps.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# In production this must be set via the SECRET_KEY environment variable.
# The fallback exists only so the app can boot in local/dev without a .env file.
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-dev-secret-key-do-not-use-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """One-way bcrypt hash. This is what gets stored in User.hashed_password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt's plaintext password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Encode `data` (in practice just {"sub": username}) into a signed JWT with
    an expiry claim. The token is opaque to the client -- it just gets echoed
    back as a Bearer header on every subsequent request.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Verify signature + expiry and return the claims, or None if invalid/expired."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

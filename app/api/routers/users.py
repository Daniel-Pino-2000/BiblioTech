"""
User accounts: registration, profile lookup/update, and credit cards.

Registration (POST /users) is public. Everything that reads or writes a
specific user's private data requires a token, and requires that token to
belong to that exact user -- see _ensure_self below. There is deliberately
no endpoint to grant admin; see scripts/make_admin.py and the README.
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.credit_card import CreditCardCreate
from app.services import credit_cards_service
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services import users_service

# Router acts as the controller layer handling HTTP requests
router = APIRouter(tags=["Users"])


def _ensure_self(username: str, current_user: User):
    """Raise 403 unless the authenticated caller *is* the account being acted on."""
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Not authorized to modify this user")


@router.get("/users/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Public profile lookup -- no auth required, no sensitive fields returned."""
    user = users_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new account. Password is hashed before it ever touches the DB."""
    if users_service.username_exists(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    return users_service.create_user(db, user)


@router.patch("/users/{username}", status_code=204)
def update_user(
    username: str,
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Partial update of the caller's own profile (name/address/password)."""
    _ensure_self(username, current_user)

    user = users_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users_service.update_user(db, user, updates)
    return Response(status_code=204)


@router.post("/users/{username}/credit-cards", status_code=201)
def add_credit_card(
    username: str,
    card: CreditCardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save a card to the caller's own account. Only the last 4 digits are persisted."""
    _ensure_self(username, current_user)

    ok = credit_cards_service.create_credit_card_for_user(db, username, card)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=201)


@router.get("/users/id/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Same as GET /users/{username}, keyed by numeric id instead."""
    user = users_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

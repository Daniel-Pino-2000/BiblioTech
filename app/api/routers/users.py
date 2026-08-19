# Router handles HTTP requests and responses

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Response
from app.schemas.credit_card import CreditCardCreate
from app.services import credit_cards_service
from app.database import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services import users_service

# Router acts as the controller layer handling HTTP requests
router = APIRouter(tags=["Users"])

# Retrieve a user by username
@router.get("/users/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = users_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Router handles HTTP requests and responses
# Create a new user
@router.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # Check if username already exists
    if users_service.username_exists(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if username already exists
    users_service.create_user(db, user)
    
    # Call service layer to create user
    return Response(status_code=201)  # truly empty body

# Validate that username is unique
@router.patch("/users/{username}", status_code=204)
def update_user(username: str, updates: UserUpdate, db: Session = Depends(get_db)):
    user = users_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update existing user fields
    users_service.update_user(db, user, updates)
    return Response(status_code=204)

# Call service to update user data
@router.post("/users/{username}/credit-cards", status_code=201)
def add_credit_card(username: str, card: CreditCardCreate, db: Session = Depends(get_db)):
    ok = credit_cards_service.create_credit_card_for_user(db, username, card)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=201)


@router.get("/users/id/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = users_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# Service layer contains business logic and DB operations

from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# Retrieve a user by username
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

# Check if a username already exists in the database
def username_exists(db: Session, username: str) -> bool:
    return db.query(User).filter(User.username == username).first() is not None

# Create a new user in the database
def create_user(db: Session, data: UserCreate) -> User:

    # Create SQLAlchemy User object with a hashed password
    new_user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
        name=data.name,
        email=data.email,
        address=data.address,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update user fields (partial update)
def update_user(db: Session, user: User, updates: UserUpdate) -> User:
    # only update fields that were provided
    if updates.password is not None:
        user.hashed_password = hash_password(updates.password)
    if updates.name is not None:
        user.name = updates.name
    if updates.address is not None:
        user.address = updates.address

    db.commit()  # Save changes
    db.refresh(user)
    return user

# Retrieve a user by ID
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# Verify a username/password pair, returning the user if valid
def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

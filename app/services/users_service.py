# Service layer contains business logic and DB operations

from sqlalchemy.orm import Session
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
    
    # Create SQLAlchemy User object
    new_user = User(
        username=data.username,
        password=data.password,   # later: hash this
        name=data.name,
        email=data.email,
        address=data.address,
    )
    
    # Create SQLAlchemy User object
    db.add(new_user) # Add to session
    db.commit() # Add to session
    
    
    db.refresh(new_user) # Refresh instance with DB values
    return new_user

# Update user fields (partial update)
def update_user(db: Session, user: User, updates: UserUpdate) -> User:
    # only update fields that were provided
    if updates.password is not None:
        user.password = updates.password
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

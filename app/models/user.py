from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.database import Base

# Always close session after request
class User(Base):
    __tablename__ = "users"

    # SQLAlchemy model representing the "users" table
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Unique username used for login/identification
    username = Column(String(50), nullable=False, unique=True, index=True)
    
    # Password stored in database (should be hashed in real applications)
    password = Column(String(255), nullable=False)   # stored in DB, but we won't return it
    
    # Optional user information
    name = Column(String(100))
    email = Column(String(100))
    address = Column(String(255))
    
    # Optional user information
    credit_cards = relationship(
        "CreditCard",
        back_populates="user",
        cascade="all, delete-orphan"
    )
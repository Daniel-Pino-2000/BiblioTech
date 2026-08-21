from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base

# Always close session after request
class User(Base):
    __tablename__ = "users"

    # SQLAlchemy model representing the "users" table
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Unique username used for login/identification
    username = Column(String(50), nullable=False, unique=True, index=True)

    # Bcrypt password hash (never store or return the raw password)
    hashed_password = Column(String(255), nullable=False)

    # Grants access to admin-only endpoints (catalog management)
    is_admin = Column(Boolean, nullable=False, default=False)

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
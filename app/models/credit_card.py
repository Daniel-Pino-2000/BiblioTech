from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Relationship: one user can have many credit cards
class CreditCard(Base):
    __tablename__ = "credit_cards"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key linking credit card to a user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Only the last 4 digits are retained; the full PAN is never persisted.
    last4 = Column(String(4), nullable=False)
    card_holder_name = Column(String(100), nullable=False)
    exp_month = Column(Integer, nullable=False)
    exp_year = Column(Integer, nullable=False)

    # Relationship back to the User model
    user = relationship("User", back_populates="credit_cards")

from sqlalchemy import Column, Integer, ForeignKey, String
from app.database import Base

class Wishlist(Base):
    """A named list of books. Capped at 3 per user (enforced in wishlist_service,
    not here -- SQLAlchemy models hold schema, not business rules)."""

    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)

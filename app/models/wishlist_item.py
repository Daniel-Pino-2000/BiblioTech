from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class WishlistItem(Base):
    """One book on one wishlist. The `book` relationship is what lets
    WishlistItemResponse nest full book details instead of just book_id."""

    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))

    book = relationship("Book")

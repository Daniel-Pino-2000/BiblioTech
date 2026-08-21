from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Author(Base):
    """An author. Optional on Book (author_id is nullable, ON DELETE SET NULL) --
    a book doesn't stop existing if its author record is removed."""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    biography = Column(Text)
    publisher = Column(Text)

    books = relationship("Book", back_populates="author")
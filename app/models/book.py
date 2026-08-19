from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    """
    Represents a book entity in the system.

    This table stores all relevant information about books, including
    their metadata (title, genre, publisher), pricing, and relationships
    to authors and ratings.
    """
    __tablename__ = "books"

    # Primary key: unique identifier for each book
    id = Column(Integer, primary_key=True, index=True)

    # International Standard Book Number (must be unique)
    isbn = Column(String(20), nullable=False, unique=True)

    # Title of the book
    title = Column(String(255), nullable=False)

    # Optional description or summary of the book
    description = Column(Text)

    # Price of the book (up to 10 digits, 2 decimal places)
    price = Column(DECIMAL(10, 2), nullable=False)

    # Genre/category of the book (e.g., Fiction, Science, etc.)
    genre = Column(String(100))

    # Publisher name
    publisher = Column(String(100))

    # Year the book was published
    year_published = Column(Integer)

    # Total number of copies sold (default is 0)
    copies_sold = Column(Integer, default=0)

    # Foreign key referencing the Author table
    # If the author is deleted, this field is set to NULL
    author_id = Column(
        Integer,
        ForeignKey("authors.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relationship to Author model (one author -> many books)
    author = relationship("Author", back_populates="books")

    # Relationship to Rating model (one book -> many ratings)
    ratings = relationship("Rating", back_populates="book")
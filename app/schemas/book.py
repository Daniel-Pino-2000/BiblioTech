from decimal import Decimal

from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    isbn: str
    title: str
    description: Optional[str] = None
    price: Decimal
    genre: Optional[str] = None
    publisher: Optional[str] = None
    year_published: Optional[int] = None
    copies_sold: Optional[int] = None
    author_id: Optional[int] = None

class BookResponse(BaseModel):
    """
    Represents the response schema for a book.

    This model is used to return book data from the API, including
    optional fields and computed values such as the average rating.
    """

    # Unique identifier of the book
    id: int

    # International Standard Book Number
    isbn: str

    # Title of the book
    title: str

    # Optional description or summary
    description: Optional[str]

    # Price of the book
    price: Decimal

    # Optional genre/category
    genre: Optional[str]

    # Optional publisher name
    publisher: Optional[str]

    # Optional year the book was published
    year_published: Optional[int]

    # Total number of copies sold
    copies_sold: int

    # Reference to the author (can be null)
    author_id: Optional[int]

    # Computed field: average rating of the book (if available)
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True

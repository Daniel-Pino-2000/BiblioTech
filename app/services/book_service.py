"""Catalog queries and mutations: browsing/search/filtering, admin writes
(create_book, discount_books_by_publisher), and the rating-join used by
get_books_by_min_rating."""

from decimal import Decimal

from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.author import Author

from sqlalchemy import func
from app.models.rating import Rating

from app.schemas.book import BookCreate


def list_books(db: Session, search: str | None = None, genre: str | None = None, skip: int = 0, limit: int = 20):
    """
    Browse/search the catalog with optional filters and pagination.

    Args:
        db: SQLAlchemy session used to query the database.
        search: Optional case-insensitive substring match against the title.
        genre: Optional exact genre filter.
        skip: Number of results to skip (pagination offset).
        limit: Maximum number of results to return.

    Returns:
        A list of Book objects matching the given filters.
    """
    query = db.query(Book)

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    if genre:
        query = query.filter(Book.genre == genre)

    return query.order_by(Book.title).offset(skip).limit(limit).all()


def get_books_by_genre(db: Session, genre: str):
    """
    Retrieve all books that belong to a specific genre.

    Args:
        db: SQLAlchemy session used to query the database.
        genre: Genre to filter books by.

    Returns:
        A list of Book objects matching the given genre.
    """
    return (
        db.query(Book)
        .filter(Book.genre == genre)
        .all()
    )


def get_top_sellers(db: Session):
    """
    Retrieve the top 10 best-selling books based on copies sold.

    Args:
        db: SQLAlchemy session used to query the database.

    Returns:
        A list of the top 10 Book objects ordered by copies_sold (descending).
    """
    return (
        db.query(Book)
        .order_by(Book.copies_sold.desc())
        .limit(10)
        .all()
    )


def discount_books_by_publisher(db: Session, publisher: str, discount: float):
    """
    Apply a percentage discount to all books from a specific publisher.

    Args:
        db: SQLAlchemy session used to update the database.
        publisher: Name of the publisher whose books will be discounted.
        discount: Discount percentage (must be between 0 and 100).

    Raises:
        ValueError: If the discount is not within the valid range.

    Side Effects:
        Updates the price of matching books and commits the changes to the database.
    """
    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")

    discount_factor = Decimal(1) - Decimal(discount) / Decimal(100)

    books = db.query(Book).filter(Book.publisher == publisher).all()

    for book in books:
        book.price = book.price * discount_factor # type: ignore

    db.commit()


def get_books_by_min_rating(db: Session, min_rating: float):
    """
    Retrieve books whose average rating meets or exceeds a minimum threshold.

    Args:
        db: SQLAlchemy session used to query the database.
        min_rating: Minimum average rating required.

    Returns:
        A list of Book objects with an added 'average_rating' attribute.
    """
    results = (
        db.query(
            Book,
            func.avg(Rating.rating).label("average_rating")
        )
        .join(Rating, Rating.book_id == Book.id)
        .group_by(Book.id)
        .having(func.avg(Rating.rating) >= min_rating)
        .all()
    )

    books = []
    for book, avg_rating in results:
        book.average_rating = round(avg_rating, 2)
        books.append(book)

    return books

# Insert a new book record into the database
def create_book(db: Session, book: BookCreate):
    new_book = Book(
        isbn=book.isbn,
        title=book.title,
        description=book.description,
        price=book.price,
        genre=book.genre,
        publisher=book.publisher,
        year_published=book.year_published,
        copies_sold=book.copies_sold,
        author_id=book.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Fetch a book from the database by its ISBN
def get_book_by_isbn(db: Session, isbn: str):
    return db.query(Book).filter(Book.isbn == isbn).first()

# Fetch a book from the database by its numeric ID
def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

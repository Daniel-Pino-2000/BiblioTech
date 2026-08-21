"""
Catalog browsing (public) and catalog management (admin-only).

Route order matters here: FastAPI matches path templates top-to-bottom, so
the static prefixes (/genre/{genre}, /top-sellers, /create-book, /id/{id})
are registered before the catch-all /{isbn} -- otherwise a request like
GET /books/top-sellers would get swallowed by get_book(isbn="top-sellers").
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_admin_user
from app.models.user import User
from app.schemas.book import BookCreate, BookResponse
from app.services import book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=list[BookResponse], response_model_exclude_none=True)
def list_books(
    search: str | None = None,
    genre: str | None = None,
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """Browse/search the full catalog: optional title substring + genre filter, paginated."""
    return book_service.list_books(db, search=search, genre=genre, skip=skip, limit=limit)


@router.get("/genre/{genre}", response_model=list[BookResponse], response_model_exclude_none=True)
def browse_by_genre(genre: str, db: Session = Depends(get_db)):
    """Exact-match genre filter (unpaginated -- kept from the original course version)."""
    return book_service.get_books_by_genre(db, genre)


@router.get("/top-sellers", response_model=list[BookResponse], response_model_exclude_none=True)
def top_sellers(db: Session = Depends(get_db)):
    """The 10 books with the highest copies_sold."""
    return book_service.get_top_sellers(db)


@router.patch("/discount")
def discount_books(
    publisher: str,
    discount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Admin-only: apply a percentage discount to every book from one publisher."""
    book_service.discount_books_by_publisher(db, publisher, discount)
    return {"message": "Discount applied successfully"}


@router.get("/rating/{min_rating}", response_model=list[BookResponse])
def browse_by_rating(min_rating: float, db: Session = Depends(get_db)):
    """Books whose average rating is >= min_rating."""
    return book_service.get_books_by_min_rating(db, min_rating)


@router.post("/create-book", response_model=BookResponse, status_code=201)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Admin-only: add a new book to the catalog. Backs the frontend's /admin page."""
    return book_service.create_book(db, book)


@router.get("/id/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """Fetch a single book by its numeric id (used by cart/wishlist nested responses)."""
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/{isbn}", response_model=BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    """Fetch a single book by ISBN -- what the frontend's book detail page uses."""
    book = book_service.get_book_by_isbn(db, isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_admin_user
from app.models.user import User
from app.schemas.book import BookCreate, BookResponse
from app.services import book_service

router = APIRouter(prefix="/books", tags=["Books"])

# Browse/search the catalog with optional filters and pagination
@router.get("", response_model=list[BookResponse], response_model_exclude_none=True)
def list_books(
    search: str | None = None,
    genre: str | None = None,
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    return book_service.list_books(db, search=search, genre=genre, skip=skip, limit=limit)

@router.get("/genre/{genre}", response_model=list[BookResponse], response_model_exclude_none=True)
def browse_by_genre(genre: str, db: Session = Depends(get_db)):
    return book_service.get_books_by_genre(db, genre)

@router.get("/top-sellers", response_model=list[BookResponse], response_model_exclude_none=True)
def top_sellers(db: Session = Depends(get_db)):
    return book_service.get_top_sellers(db)

@router.patch("/discount")
def discount_books(
    publisher: str,
    discount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    book_service.discount_books_by_publisher(db, publisher, discount)
    return {"message": "Discount applied successfully"}

@router.get("/rating/{min_rating}", response_model=list[BookResponse])
def browse_by_rating(min_rating: float, db: Session = Depends(get_db)):
    return book_service.get_books_by_min_rating(db, min_rating)

# Create a new book and save it to the database (admin-only action)
@router.post("/create-book", response_model=BookResponse, status_code=201)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    return book_service.create_book(db, book)

# Retrieve a book using its numeric ID
@router.get("/id/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Retrieve a book using its ISBN
@router.get("/{isbn}", response_model=BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = book_service.get_book_by_isbn(db, isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

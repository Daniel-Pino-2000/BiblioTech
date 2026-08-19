from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.book import BookCreate, BookResponse
from app.services import book_service

router = APIRouter(prefix="/books", tags=["Books"])

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
    db: Session = Depends(get_db)
):
    book_service.discount_books_by_publisher(db, publisher, discount)
    return {"message": "Discount applied successfully"}

@router.get("/rating/{min_rating}", response_model=list[BookResponse])
def browse_by_rating(min_rating: float, db: Session = Depends(get_db)):
    return book_service.get_books_by_min_rating(db, min_rating)

# Create a new book and save it to the database
@router.post("/create-book", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)

# Retrieve a book using its ISBN
@router.get("/{isbn}", response_model=BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    return book_service.get_book_by_isbn(db, isbn)
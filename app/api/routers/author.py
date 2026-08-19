from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.author import AuthorCreate, AuthorResponse
from app.schemas.book import BookResponse
from app.services import author_service

router = APIRouter(prefix="/authors", tags=["Authors"])

# Create a new author and store it in the database
@router.post("/create-author", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return author_service.create_author(db, author)

# Get all books associated with a specific author ID
@router.get("/{author_id}/books", response_model=list[BookResponse], response_model_exclude_none=True)
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return author_service.get_books_by_author_id(db, author_id)

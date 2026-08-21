"""Author records. Deliberately minimal -- there's no list-all-authors
endpoint, since the only current consumer (the admin book form) treats
author_id as optional and doesn't need to browse them."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_admin_user
from app.models.user import User
from app.schemas.author import AuthorCreate, AuthorResponse
from app.schemas.book import BookResponse
from app.services import author_service

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/create-author", response_model=AuthorResponse, status_code=201)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Admin-only: add a new author, referenceable from BookCreate.author_id."""
    return author_service.create_author(db, author)


@router.get("/{author_id}/books", response_model=list[BookResponse], response_model_exclude_none=True)
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    """All books by one author. Public -- no auth required."""
    return author_service.get_books_by_author_id(db, author_id)

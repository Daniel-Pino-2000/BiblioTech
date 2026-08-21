"""Author records -- deliberately the thinnest service in the app (see
routers/author.py for why there's no list-all endpoint)."""

from sqlalchemy.orm import Session
from app.models import Author, Book

from sqlalchemy import func

from app.schemas.author import AuthorCreate

# Insert a new author into the database
def create_author(db: Session, author: AuthorCreate):
    author = Author(
        first_name=author.first_name,
        last_name=author.last_name,
        biography=author.biography,
        publisher=author.publisher
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author
 
 # Retrieve all books for a given author ID
def get_books_by_author_id(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id == author_id).all()
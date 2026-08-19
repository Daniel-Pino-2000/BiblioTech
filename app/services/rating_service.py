from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.rating import Rating
from app.models.comment import Comment
from app.services.users_service import get_user_by_id
from typing import cast

"""
rating_service.py

Contains all business logic related to ratings and comments.
Routers should call these functions instead of directly querying the database.
This ensures separation of concerns and keeps business logic centralized.
"""

# Constants used for error handling across the service layer
USER_NOT_FOUND = "USER_NOT_FOUND"
EMPTY_TEXT = "EMPTY_TEXT"


def create_rating(db: Session, user_id: int, book_id: int, rating_value: int):
    """
    Create or update a rating for a specific book.

    Process:
        - Validate that the user exists
        - Check if the user already rated the book
        - If rating exists → update it
        - Otherwise → create a new rating

    Args:
        db: Database session
        user_id: ID of the user submitting the rating
        book_id: ID of the book being rated
        rating_value: Rating value (expected 0–5)

    Returns:
        Rating object (new or updated)
    """

    # Validate that the user exists before proceeding
    validate_user(db, user_id)
    
    # Check if a rating already exists for this user and book
    existing_rating = db.query(Rating).filter(
        Rating.user_id == user_id,
        Rating.book_id == book_id,
    ).first()

    # If rating exists → update the existing record
    if existing_rating:
        cast(Rating, existing_rating).rating = rating_value  # type:ignore[attr-defined]
        db.commit()
        db.refresh(existing_rating)
        return existing_rating

    # Otherwise → create a new rating
    rating = Rating(user_id=user_id, book_id=book_id, rating=rating_value)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating



def create_comment(db: Session, user_id: int, book_id: int, text: str):
    """
    Create a new comment for a specific book.

    Process:
        - Validate that the user exists
        - Ensure comment text is not empty
        - Store the comment in the database

    Args:
        db: Database session
        user_id: ID of the user submitting the comment
        book_id: ID of the book being commented on
        text: Comment content

    Returns:
        Comment object
    """

    # Validate that the user exists
    validate_user(db, user_id)
    
    # Ensure comment is not empty or just whitespace
    if not text.strip():
        raise ValueError(EMPTY_TEXT)

    # Create and persist the comment
    comment = Comment(
        user_id=user_id,
        book_id=book_id,
        comment=text
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_book_comments(db: Session, book_id: int):
    """
    Retrieve all comments for a specific book.

    Args:
        db: Database session
        book_id: ID of the book

    Returns:
        List of Comment objects
    """
    return db.query(Comment).filter(Comment.book_id == book_id).all()



def get_average_rating(db: Session, book_id: int):
    """
    Calculate the average rating for a specific book.

    Process:
        - Use SQL aggregation function (AVG)
        - Return 0.0 if no ratings exist

    Args:
        db: Database session
        book_id: ID of the book

    Returns:
        Float value representing average rating
    """

    avg = db.query(func.avg(Rating.rating))\
        .filter(Rating.book_id == book_id)\
        .scalar()
    
    # Convert result to float and round to 2 decimal places
    return round(float(avg), 2) if avg else 0.0


def validate_user(db: Session, user_id: int):
    """
    Validate that a user exists in the system.

    Args:
        db: Database session
        user_id: ID of the user

    Raises:
        ValueError: If user does not exist

    Returns:
        User object if valid
    """

    user = get_user_by_id(db, user_id)

    # Raise error if user is not found
    if not user:
        raise ValueError(USER_NOT_FOUND)

    return user
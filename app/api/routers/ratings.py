from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.rating import RatingCreate, RatingResponse
from app.schemas.comment import CommentCreate, CommentResponse
from app.services import rating_service


# Router responsible for handling all rating and commenting related endpoints
router = APIRouter(
    prefix="/books",
    tags=["Ratings & Comments"]
)


@router.post("/{book_id}/ratings", response_model=RatingResponse)
def add_rating(
    book_id: int,
    data: RatingCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update a rating for a specific book.

    Path Parameters:
        book_id: ID of the book to be rated

    Request Body:
        data: Contains user_id and rating value

    Process:
        - Delegates logic to the rating service
        - Service handles validation and database operations

    Returns:
        The created or updated rating object
    """
    try:
        return rating_service.create_rating(
            db,
            data.user_id,
            book_id,
            data.rating
        )

    # Handle known business errors from the service layer
    except ValueError as e:
        if str(e) == rating_service.USER_NOT_FOUND:
            raise HTTPException(404, "User not found")

        # Generic fallback for unexpected errors
        raise HTTPException(500, "Unexpected error")
    

@router.post("/{book_id}/comments", response_model=CommentResponse)
def add_comment(
    book_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new comment for a specific book.

    Path Parameters:
        book_id: ID of the book being commented on

    Request Body:
        data: Contains user_id and comment text

    Process:
        - Validates user existence
        - Validates that comment is not empty
        - Stores comment in the database

    Returns:
        The created comment object
    """
    try:
        return rating_service.create_comment(
            db,
            data.user_id,
            book_id,
            data.comment
        )

    # Handle specific validation errors from service layer
    except ValueError as e:
        if str(e) == rating_service.USER_NOT_FOUND:
            raise HTTPException(404, "User not found")

        if str(e) == rating_service.EMPTY_TEXT:
            raise HTTPException(400, "Comment cannot be empty")

        # Generic fallback error
        raise HTTPException(500, "Unexpected error")
    

@router.get("/{book_id}/comments",
            response_model=list[CommentResponse])
def get_comments(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all comments for a specific book.

    Path Parameters:
        book_id: ID of the book

    Returns:
        A list of comments associated with the book
    """
    return rating_service.get_book_comments(db, book_id)


@router.get("/{book_id}/ratings/average")
def get_average_rating(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve the average rating for a specific book.

    Path Parameters:
        book_id: ID of the book

    Process:
        - Calculates average rating using service layer
        - Returns 0 if no ratings exist

    Returns:
        JSON object with book_id and average_rating
    """
    avg = rating_service.get_average_rating(db, book_id)

    return {
        "book_id": book_id,
        "average_rating": avg
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.wishlist import (
    WishlistCreate, 
    WishlistResponse,
    WishlistItemResponse,
    AddBookToWishlist
)
from app.services import wishlist_service

# Router responsible for all wishlist-related operations
router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


# Create a new wishlist for a user
@router.post("/", response_model=WishlistResponse)
def create_wishlist(data: WishlistCreate, db: Session = Depends(get_db)):
    """
    Create a new wishlist.

    Request Body:
        data: Contains user_id and wishlist name

    Process:
        - Validates that the user exists
        - Ensures wishlist name is not empty
        - Ensures user has not exceeded the maximum number of wishlists (e.g., 3)

    Returns:
        The created wishlist object
    """
    try:
        return wishlist_service.create_wishlist(
            db,
            data.user_id,
            data.name
        )

    # Handle known validation errors from service layer
    except ValueError as e:

        if str(e) == wishlist_service.USER_NOT_FOUND:
            raise HTTPException(404, "User not found")

        if str(e) == wishlist_service.EMPTY_TEXT:
            raise HTTPException(400, "Wishlist name cannot be empty")

        if str(e) == wishlist_service.MAX_WISHLISTS_REACHED:
            raise HTTPException(400, "User can only have 3 wishlists")

        # Generic fallback error
        raise HTTPException(500, "Unexpected error")


# Add a book to a wishlist
@router.post("/add-book")
@router.post("/items", response_model=WishlistItemResponse)
def add_book(data: AddBookToWishlist, db: Session = Depends(get_db)):
    """
    Add a book to a specific wishlist.

    Request Body:
        data: Contains wishlist_id and book_id

    Process:
        - Validates that the wishlist exists
        - Prevents duplicate books in the same wishlist
        - Creates a WishlistItem record in the database

    Returns:
        The created wishlist item
    """
    try:
        return wishlist_service.add_book_to_wishlist(
            db,
            data.wishlist_id,
            data.book_id
        )

    # Handle validation errors from service layer
    except ValueError as e:

        if str(e) == wishlist_service.WISHLIST_NOT_FOUND:
            raise HTTPException(404, "Wishlist not found")
        
        if str(e) == wishlist_service.BOOK_ALREADY_IN_WISHLIST:
            raise HTTPException(
                status_code=400,
                detail="Book already exists in wishlist"
            )

        raise HTTPException(500, "Unexpected error")


# Retrieve all wishlists for a specific user
@router.get("/user/{user_id}", response_model=list[WishlistResponse])
def get_user_lists(user_id: int, db: Session = Depends(get_db)):
    """
    Get all wishlists belonging to a user.

    Path Parameters:
        user_id: ID of the user

    Returns:
        List of wishlists associated with the user
    """
    try:
        return wishlist_service.get_user_wishlists(db, user_id)

    except ValueError:
        raise HTTPException(404, "User not found")


# Retrieve all books in a specific wishlist
@router.get("/{wishlist_id}", response_model=list[WishlistItemResponse])
def get_books(wishlist_id: int, db: Session = Depends(get_db)):
    """
    Get all books inside a specific wishlist.

    Path Parameters:
        wishlist_id: ID of the wishlist

    Returns:
        List of books (wishlist items)
    """
    try:
        return wishlist_service.get_books_in_wishlist(db, wishlist_id)

    except ValueError:
        raise HTTPException(404, "Wishlist not found")


# Remove a book from a wishlist
@router.delete("/{wishlist_id}/items/{book_id}")
def remove_book(
    wishlist_id: int,
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove a book from a wishlist.

    Path Parameters:
        wishlist_id: ID of the wishlist
        book_id: ID of the book to remove

    Process:
        - Validates that the wishlist and item exist
        - Deletes the corresponding WishlistItem from the database

    Returns:
        Confirmation message
    """
    try:
        wishlist_service.remove_book(db, wishlist_id, book_id)
        return {"message": "Book removed successfully"}

    except ValueError:
        raise HTTPException(404, "Item not found")
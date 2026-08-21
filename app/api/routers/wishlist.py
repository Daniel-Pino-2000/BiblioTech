from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.wishlist import (
    WishlistCreate,
    WishlistResponse,
    WishlistItemResponse,
    AddBookToWishlist
)
from app.services import wishlist_service

# Router responsible for all wishlist-related operations
router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


def _ensure_owns_wishlist(db: Session, wishlist_id: int, current_user: User):
    wishlist = wishlist_service.get_wishlist_by_id(db, wishlist_id)
    if not wishlist:
        raise HTTPException(404, "Wishlist not found")
    if wishlist.user_id != current_user.id:
        raise HTTPException(403, "Not authorized to access this wishlist")
    return wishlist


# Create a new wishlist for the authenticated user
@router.post("/", response_model=WishlistResponse)
def create_wishlist(
    data: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new wishlist for the authenticated user.

    Process:
        - Ensures wishlist name is not empty
        - Ensures user has not exceeded the maximum number of wishlists (e.g., 3)

    Returns:
        The created wishlist object
    """
    try:
        return wishlist_service.create_wishlist(
            db,
            current_user.id,
            data.name
        )

    # Handle known validation errors from service layer
    except ValueError as e:

        if str(e) == wishlist_service.EMPTY_TEXT:
            raise HTTPException(400, "Wishlist name cannot be empty")

        if str(e) == wishlist_service.MAX_WISHLISTS_REACHED:
            raise HTTPException(400, "User can only have 3 wishlists")

        if str(e) == wishlist_service.WISHLIST_ALREADY_EXISTS:
            raise HTTPException(400, "A wishlist with that name already exists")

        # Generic fallback error
        raise HTTPException(500, "Unexpected error")


# Add a book to one of the authenticated user's wishlists
@router.post("/items", response_model=WishlistItemResponse)
def add_book(
    data: AddBookToWishlist,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a book to a specific wishlist owned by the authenticated user.

    Process:
        - Validates that the wishlist exists and belongs to the caller
        - Prevents duplicate books in the same wishlist
        - Creates a WishlistItem record in the database

    Returns:
        The created wishlist item
    """
    _ensure_owns_wishlist(db, data.wishlist_id, current_user)

    try:
        return wishlist_service.add_book_to_wishlist(
            db,
            data.wishlist_id,
            data.book_id
        )

    # Handle validation errors from service layer
    except ValueError as e:

        if str(e) == wishlist_service.BOOK_ALREADY_IN_WISHLIST:
            raise HTTPException(
                status_code=400,
                detail="Book already exists in wishlist"
            )

        raise HTTPException(500, "Unexpected error")


# Retrieve all wishlists for the authenticated user
@router.get("/user/{user_id}", response_model=list[WishlistResponse])
def get_user_lists(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all wishlists belonging to a user.

    Path Parameters:
        user_id: ID of the user (must match the authenticated user)

    Returns:
        List of wishlists associated with the user
    """
    if current_user.id != user_id:
        raise HTTPException(403, "Not authorized to view these wishlists")

    try:
        return wishlist_service.get_user_wishlists(db, user_id)

    except ValueError:
        raise HTTPException(404, "User not found")


# Retrieve all books in a specific wishlist owned by the authenticated user
@router.get("/{wishlist_id}", response_model=list[WishlistItemResponse])
def get_books(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all books inside a specific wishlist.

    Path Parameters:
        wishlist_id: ID of the wishlist (must belong to the authenticated user)

    Returns:
        List of books (wishlist items)
    """
    _ensure_owns_wishlist(db, wishlist_id, current_user)
    return wishlist_service.get_books_in_wishlist(db, wishlist_id)


# Remove a book from a wishlist owned by the authenticated user
@router.delete("/{wishlist_id}/items/{book_id}")
def remove_book(
    wishlist_id: int,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Remove a book from a wishlist.

    Path Parameters:
        wishlist_id: ID of the wishlist (must belong to the authenticated user)
        book_id: ID of the book to remove

    Returns:
        Confirmation message
    """
    _ensure_owns_wishlist(db, wishlist_id, current_user)

    try:
        wishlist_service.remove_book(db, wishlist_id, book_id)
        return {"message": "Book removed successfully"}

    except ValueError:
        raise HTTPException(404, "Item not found")

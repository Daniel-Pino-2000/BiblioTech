"""
wishlist_service.py

Contains all business logic related to wishlist management.
Responsible for validation, enforcing business rules, and interacting with the database.
Routers should delegate operations to this service instead of handling logic directly.

Ownership (does this wishlist belong to the caller?) is checked by the router,
not here -- this module only enforces business rules that hold regardless of
who's asking (max 3 wishlists, no duplicate names, no duplicate books).
"""

from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist
from app.models.wishlist_item import WishlistItem
from app.services.users_service import get_user_by_id

# Error constants used for consistent error handling
USER_NOT_FOUND = "USER NOT FOUND"
EMPTY_TEXT = "EMPTY TEXT"
WISHLIST_NOT_FOUND = "WISHLIST NOT FOUND"
BOOK_NOT_IN_WISHLIST = "BOOK_NOT_IN_WISHLIST"
MAX_WISHLISTS_REACHED = "MAX WISHLISTS REACHED"
WISHLIST_ALREADY_EXISTS = "WISHLIST_ALREADY_EXISTS"
BOOK_ALREADY_IN_WISHLIST = "BOOK ALREADY IN WISHLIST"


def create_wishlist(db: Session, user_id: int, name: str):
    """
    Create a new wishlist for a user.

    Business Rules:
        - User must exist
        - Wishlist name cannot be empty
        - A user can have a maximum of 3 wishlists
        - Duplicate wishlist names are not allowed per user

    Args:
        db: Database session
        user_id: ID of the user
        name: Wishlist name

    Returns:
        Newly created Wishlist object
    """

    # Validate user existence
    validate_user(db, user_id)

    # Ensure name is not empty or whitespace
    if not name or name.strip() == "":
        raise ValueError(EMPTY_TEXT)
    
    # Enforce maximum number of wishlists per user
    wishlist_count = db.query(Wishlist)\
        .filter(Wishlist.user_id == user_id)\
        .count()

    if wishlist_count >= 3:
        raise ValueError(MAX_WISHLISTS_REACHED)

    # Check for duplicate wishlist name for the same user
    duplicated_wishlist(db, user_id, name)

    # Create and persist the wishlist
    wishlist = Wishlist(user_id=user_id, name=name)
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return wishlist


def add_book_to_wishlist(db: Session, wishlist_id: int, book_id: int):
    """
    Add a book to a wishlist.

    Business Rules:
        - Wishlist must exist
        - The same book cannot be added twice

    Args:
        db: Database session
        wishlist_id: ID of the wishlist
        book_id: ID of the book

    Returns:
        Newly created WishlistItem object
    """

    # Validate wishlist existence
    validate_wishlist(db, wishlist_id)

    # Check if the book is already in the wishlist
    existing_item = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist_id,
        WishlistItem.book_id == book_id
    ).first()

    if existing_item:
        raise ValueError(BOOK_ALREADY_IN_WISHLIST)

    # Create and persist the wishlist item
    item = WishlistItem(wishlist_id=wishlist_id, book_id=book_id)
    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_user_wishlists(db: Session, user_id: int):
    """
    Retrieve all wishlists for a specific user.

    Args:
        db: Database session
        user_id: ID of the user

    Returns:
        List of Wishlist objects
    """

    # Ensure user exists before querying
    validate_user(db, user_id)

    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()


def get_books_in_wishlist(db: Session, wishlist_id: int):
    """
    Retrieve all books (wishlist items) in a specific wishlist.

    Args:
        db: Database session
        wishlist_id: ID of the wishlist

    Returns:
        List of WishlistItem objects
    """

    # Validate wishlist existence
    validate_wishlist(db, wishlist_id)

    return db.query(WishlistItem)\
        .filter(WishlistItem.wishlist_id == wishlist_id)\
        .all()


def remove_book(db: Session, wishlist_id: int, book_id: int):
    """
    Remove a book from a wishlist.

    Business Rules:
        - Wishlist must exist
        - Book must be present in the wishlist

    Args:
        db: Database session
        wishlist_id: ID of the wishlist
        book_id: ID of the book

    Raises:
        ValueError: If the book is not found in the wishlist
    """

    # Validate wishlist existence
    validate_wishlist(db, wishlist_id)
    
    # Find the specific wishlist item
    item = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist_id,
        WishlistItem.book_id == book_id
    ).first()

    # If item does not exist → raise error
    if not item:
        raise ValueError(BOOK_NOT_IN_WISHLIST)
    
    # Delete the item from the database
    db.delete(item)
    db.commit()


def get_wishlist_by_id(db: Session, wishlist_id: int) -> Wishlist | None:
    """
    Retrieve a wishlist by its ID.

    Args:
        db: Database session
        wishlist_id: ID of the wishlist

    Returns:
        Wishlist object or None if not found
    """
    return db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()


def validate_user(db: Session, user_id: int):
    """
    Validate that a user exists.

    Args:
        db: Database session
        user_id: ID of the user

    Raises:
        ValueError: If user does not exist

    Returns:
        User object if valid
    """

    user = get_user_by_id(db, user_id)

    if not user:
        raise ValueError(USER_NOT_FOUND)

    return user


def validate_wishlist(db: Session, wishlist_id: int) -> Wishlist | None:
    """
    Validate that a wishlist exists.

    Args:
        db: Database session
        wishlist_id: ID of the wishlist

    Raises:
        ValueError: If wishlist does not exist

    Returns:
        Wishlist object if valid
    """

    wishlist = get_wishlist_by_id(db, wishlist_id)

    if not wishlist:
        raise ValueError(WISHLIST_NOT_FOUND)

    return wishlist


def duplicated_wishlist(db: Session, user_id, name: str) -> Wishlist | None:
    """
    Check if a wishlist with the same name already exists for a user.

    Args:
        db: Database session
        user_id: ID of the user
        name: Wishlist name

    Raises:
        ValueError: If a duplicate wishlist is found
    """

    existing = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.name == name
    ).first()

    if existing:
        raise ValueError(WISHLIST_ALREADY_EXISTS)
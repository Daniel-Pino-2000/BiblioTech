"""
Shopping cart business logic. Every user gets exactly one ShoppingCart,
created lazily on first access (get_user_cart) rather than at registration --
there's no reason to allocate a cart row for someone who never shops.
"""

from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.cart import ShoppingCart, CartItem
from app.models.book import Book

def get_user_cart(db: Session, user_id: int):
    """Return the user's cart, creating an empty one on first access."""
    # Stores the first cart found in the database into 'cart' variable
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    
    # If there is no cart tied to the user it will add an empty cart
    if not cart:
        cart = ShoppingCart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart # cart.items will be [] at this point

def calculate_subtotal(db: Session, user_id: int):
    # Retrieves the user's cart
    cart = get_user_cart(db, user_id)

    # Calculates the subtotal by summing up the price of each cart item (uses book price * book quantity)
    subtotal = Decimal('0.00')
    for item in cart.items:
        subtotal += item.book.price * item.quantity
    return subtotal


def add_item_to_cart(db: Session, user_id: int, book_id: int):
    """Add one copy of a book to the cart, or bump quantity if it's already there."""
    # Retrieves the user's cart
    cart = get_user_cart(db, user_id)

    # Finds the desired book to add using its book ID
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return False

    # Check if the cart already has the desired book inside
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id, 
        CartItem.book_id == book_id
    ).first()

    # If cart already has desired book, add to its quantity, else create a new entry in the database for that book
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(cart_id=cart.id, book_id=book_id, quantity=1)
        db.add(new_item)

    # Make changes to the database
    db.commit()
    return True


def remove_item_from_cart(db: Session, user_id: int, book_id: int):
    """Decrement quantity by one, deleting the row entirely once it hits zero."""
    # Find the user's cart
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        return False

    # Find the specific item entry
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.book_id == book_id
    ).first()

    if existing_item:
        if existing_item.quantity > 1:
            # If more than one exists, just decrement the quantity
            existing_item.quantity -= 1
        else:
            # If only one is left, remove the entry entirely
            db.delete(existing_item)
        
        db.commit()
        return True
    
    return False
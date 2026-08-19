from pydantic import BaseModel
from app.schemas.book import BookResponse

# Schema for reading the current items in the cart, includes quantity and the book details as seen in BookResponse schema
class CartItemRead(BaseModel):
    quantity: int
    book: BookResponse

    class Config:
        from_attributes = True

# Schema that returns a lost of the books in a specific user's cart
class CartResponse(BaseModel):
    user_id: int
    user_name: str
    items: list[CartItemRead]

    class Config:
        from_attributes = True

# Schema that returns the user ID and calculated subtotal of their cart
class CartSubtotalResponse(BaseModel):
    user_id: int
    subtotal: float

# Schema for adding a book to a user's cart given book and user ID, the default quantity to add is 1 book
class CartItemCreate(BaseModel):
    user_id: int
    book_id: int
    quantity: int = 1

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.book import BookResponse


# -------------------------
# RESPONSE MODEL
# -------------------------
class WishlistResponse(BaseModel):
    id: int
    user_id: int
    name: str = Field(min_length = 1, max_length = 100)

    class Config:
        from_attributes = True


# -------------------------
# CREATE MODEL
# -------------------------
class WishlistCreate(BaseModel):
    name: str


# -------------------------
# UPDATE MODEL
# -------------------------
class WishlistUpdate(BaseModel):
    name: Optional[str] = None


# -------------------------
# ADD BOOK TO WISHLIST MODEL
# -------------------------
class AddBookToWishlist(BaseModel):
    wishlist_id: int = Field(gt = 0)
    book_id: int = Field(gt = 0)


# -------------------------
# WISHLIST ITEM CREATE MODEL
# -------------------------
class WishlistItemCreate(BaseModel):
    wishlist_id: int
    book_id: int

# -------------------------
# WISHLIST ITEMS RESPONSE MODEL
# -------------------------
class WishlistItemResponse(BaseModel):
    id: int
    wishlist_id: int
    book_id: int
    book: BookResponse

    class Config:
        from_attributes = True

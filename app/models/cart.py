from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Base shopping cart container, each user has one primary cart associated with their user ID
class ShoppingCart(Base):
    __tablename__ = "shopping_carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    
    items = relationship("CartItem", 
                         back_populates="cart", 
                         cascade="all, delete-orphan", 
                         order_by="desc(CartItem.cart_id)")

# Entry for a given item in the cart, it links a specific book to a cart using foreign keys
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("ShoppingCart", back_populates="items")
    book = relationship("Book")

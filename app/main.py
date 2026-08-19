from fastapi import FastAPI
from app.database import Base, engine
from app.api.routers.users import router as users_router
from app.api.routers.ratings import router as ratings_router
from app.api.routers.wishlist import router as wishlists_router
from app.api.routers.books import router as books_router
from app.api.routers.author import router as author_router
from app.api.routers.cart import router as cart_router

# Provides a database session for each request
app = FastAPI(title="BiblioTech API")

# Create FastAPI application instance
app.include_router(users_router)
app.include_router(author_router)
app.include_router(ratings_router)
app.include_router(wishlists_router)
app.include_router(books_router)
app.include_router(cart_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "BiblioTech API running"}

# Register routers (controllers) with the application
@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            return {"status": "ok"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


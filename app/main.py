"""
Application entrypoint: builds the FastAPI app, configures CORS, and wires up
every router. Run with `uvicorn app.main:app --reload` (see README).
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.routers.auth import router as auth_router
from app.api.routers.users import router as users_router
from app.api.routers.ratings import router as ratings_router
from app.api.routers.wishlist import router as wishlists_router
from app.api.routers.books import router as books_router
from app.api.routers.author import router as author_router
from app.api.routers.cart import router as cart_router

app = FastAPI(
    title="BiblioTech API",
    description="A RESTful backend for an online technical bookstore: catalog browsing, "
    "authentication, shopping cart, wishlists, ratings and comments.",
    version="1.0.0",
)

# Allow the frontend (served from a different origin in dev/prod) to call the API.
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (controllers) with the application
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(author_router)
app.include_router(ratings_router)
app.include_router(wishlists_router)
app.include_router(books_router)
app.include_router(cart_router)

# Tables are managed via Alembic migrations (see /alembic). This is kept as a
# convenience fallback for quick local runs against a fresh database.
if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """Liveness check with no dependencies -- just confirms the process is up."""
    return {"message": "BiblioTech API running"}


@app.get("/health")
def health():
    """Readiness check -- also confirms the database is reachable."""
    try:
        with engine.connect():
            return {"status": "ok"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

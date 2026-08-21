"""
Database connectivity: builds the SQLAlchemy engine/session factory from
environment variables and defines the declarative Base every model inherits
from. Imported by app.main, Alembic (alembic/env.py), and every service that
needs a DB session.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env file
load_dotenv()

# DATABASE_URL takes precedence (used by Docker/CI); otherwise build a MySQL
# URL from the individual DB_* variables for local development.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "bibliotech")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine (manages DB connections)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory used to create per-request DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
class Base(DeclarativeBase):
    pass

# Provides a database session for each request
def get_db():
    """
    FastAPI dependency that yields one Session per request and always closes
    it afterwards, even if the endpoint raises. Superseded by app.api.deps.get_db
    in practice (routers import from there so auth deps share the same module),
    but kept here since Alembic and ad-hoc scripts import SessionLocal directly.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

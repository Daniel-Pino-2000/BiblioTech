import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env file
load_dotenv()

# Read database configuration from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Create database connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine (manages DB connections)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create SQLAlchemy engine (manages DB connections)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
class Base(DeclarativeBase):
    pass

# Provides a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db # Base class for all ORM models
    finally:
        db.close() # Provide DB session to endpoint

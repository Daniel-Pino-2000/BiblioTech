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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

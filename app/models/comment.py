from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Comment(Base):
    """A freeform comment on a book. Unlike Rating, a user can leave any
    number of comments on the same book -- there's no uniqueness constraint."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False
    )

    comment = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
from pydantic import BaseModel, Field
from datetime import datetime

class CommentCreate(BaseModel):
    comment: str = Field(min_length=1)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

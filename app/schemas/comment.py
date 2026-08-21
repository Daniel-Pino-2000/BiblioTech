from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CommentCreate(BaseModel):
    comment: str = Field(min_length=1)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, Field

class RatingCreate(BaseModel):
    rating: int = Field(ge=0, le=5)


class RatingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int

    class Config:
        from_attributes = True

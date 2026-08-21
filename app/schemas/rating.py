from pydantic import BaseModel, Field, ConfigDict

class RatingCreate(BaseModel):
    rating: int = Field(ge=0, le=5)


class RatingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int

    model_config = ConfigDict(from_attributes=True)

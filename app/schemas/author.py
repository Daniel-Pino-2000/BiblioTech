from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None
    publisher: Optional[str] = None

class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    biography: Optional[str]
    publisher: Optional[str]

    class Config:
        from_attributes = True

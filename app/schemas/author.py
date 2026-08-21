from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

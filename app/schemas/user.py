from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class UserUpdate(BaseModel):
    password: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
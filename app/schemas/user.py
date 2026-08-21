from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_admin: bool = False

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class UserUpdate(BaseModel):
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    name: Optional[str] = None
    address: Optional[str] = None

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class BlogCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str]
    author_id: int

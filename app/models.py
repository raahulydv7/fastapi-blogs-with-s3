from pydantic import BaseModel, EmailStr
from typing import Optional



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str]
    author_id: int

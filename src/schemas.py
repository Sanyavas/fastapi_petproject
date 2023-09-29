from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

from src.database.models import Role


class PostModel(BaseModel):
    title: str = Field(max_length=256)
    post: str
    image_url: Optional[str]


class PostResponse(PostModel):
    id: int
    likes: int
    dislikes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=19)
    email: EmailStr
    password: str = Field(min_length=4, max_length=255)
    avatar: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str
    role: Role

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr

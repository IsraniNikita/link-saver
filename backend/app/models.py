from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BookmarkCreate(BaseModel):
    url: str


class BookmarkOut(BaseModel):
    id: str
    url: str
    title: Optional[str]
    favicon: Optional[str]
    summary: Optional[str]

    class Config:
        from_attributes = True


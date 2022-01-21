from typing import Optional

from pydantic import BaseModel, EmailStr

from .base import Base


class User(Base):
    name: str
    email: EmailStr


class UserCreateIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdateIn(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

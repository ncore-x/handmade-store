from typing import Optional
from pydantic import EmailStr

from src.schemas.base import BaseSchema


class AdminRequestAdd(BaseSchema):
    email: EmailStr
    password: str
    superadmin_password: str


class AdminAdd(BaseSchema):
    password: str
    superadmin_password: str


class Admin(BaseSchema):
    id: int
    email: EmailStr


class AdminWithHashedPassword(Admin):
    hashed_password: str


class AdminResponse(BaseSchema):
    id: int
    email: str
    password: Optional[str] = None
    superadmin_password: Optional[str] = None

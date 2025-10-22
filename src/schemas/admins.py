from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr, Field

from src.schemas.base import BaseSchema, TimestampSchema, IDSchema


class AdminBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    permissions: List[str] = Field(default_factory=list)


class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6)


class AdminUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    permissions: Optional[List[str]] = None


class AdminResponse(AdminBase, IDSchema, TimestampSchema):
    last_login: Optional[datetime] = None


class AdminLogin(BaseSchema):
    username: str
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    username: str | None = None

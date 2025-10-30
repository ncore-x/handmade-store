from typing import Optional
from pydantic import EmailStr, field_validator

from src.schemas.base import BaseSchema
from src.validators import validate_email_russian, validate_password_russian


class AdminRequestLogin(BaseSchema):
    email: EmailStr
    password: str

    @field_validator("email")
    def normalize_email(cls, email: str) -> str:
        return email.lower()

    _validate_email = field_validator("email")(validate_email_russian)
    _validate_password = field_validator("password")(validate_password_russian)


class AdminRequestAdd(AdminRequestLogin):
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

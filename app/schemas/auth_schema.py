import re
from uuid import UUID

from pydantic import BaseModel, Field, validator


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=128)

    @validator("name")
    def validate_name(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("Name cannot be blank")
        return name

    @validator("email")
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("Enter a valid email address")
        return email


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=128)

    @validator("email")
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("Enter a valid email address")
        return email


class   UserResponse(BaseModel):
    id: UUID
    name: str
    email: str


class LoginResponse(BaseModel):
    message:str
    access_token: str
    token_type: str

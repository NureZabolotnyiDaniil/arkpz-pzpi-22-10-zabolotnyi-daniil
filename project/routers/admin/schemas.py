from typing import Optional
from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):
    first_name: str
    surname: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminOut(BaseModel):
    id: int
    first_name: str
    surname: str
    email: EmailStr
    status: str
    rights: str

    class Config:
        from_attributes = True


class AdminUpdate(BaseModel):
    first_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


class AdminStatusUpdate(BaseModel):
    status: str = "active"
    rights: str = "restricted_access"

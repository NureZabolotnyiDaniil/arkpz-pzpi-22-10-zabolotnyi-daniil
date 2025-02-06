from typing import Optional

from pydantic import BaseModel, EmailStr


class CompanyOut(BaseModel):
    id: int
    name: Optional[str]
    email: EmailStr
    address: Optional[str]
    notes: Optional[str]

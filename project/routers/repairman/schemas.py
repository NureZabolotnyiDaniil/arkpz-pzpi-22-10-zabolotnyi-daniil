from typing import Optional

from pydantic import BaseModel, EmailStr


class RepairmanOut(BaseModel):
    id: int
    first_name: str
    surname: str
    email: EmailStr
    company_id: Optional[int]

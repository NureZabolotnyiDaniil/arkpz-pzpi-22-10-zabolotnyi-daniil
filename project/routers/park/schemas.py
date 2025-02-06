from pydantic import BaseModel


class ParkOut(BaseModel):
    id: int
    name: str
    address: str
    admin_id: int

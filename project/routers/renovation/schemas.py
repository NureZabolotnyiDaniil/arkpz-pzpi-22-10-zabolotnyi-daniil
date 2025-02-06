from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RenovationOut(BaseModel):
    id: int
    lantern_id: int
    date: datetime
    status: str
    cost: int
    repairman_id: Optional[int]


class RenovationStatus(str, Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    CANCELED = "canceled"

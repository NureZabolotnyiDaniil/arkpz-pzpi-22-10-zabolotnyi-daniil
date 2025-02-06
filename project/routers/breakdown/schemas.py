from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BreakdownOut(BaseModel):
    id: int
    lantern_id: int
    date: datetime
    description: Optional[str]

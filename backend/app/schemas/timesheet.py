from pydantic import BaseModel
from typing import Optional

class TimesheetCreate(BaseModel):
    user_id: str
    email: str
    date: str
    hours: str
    description: str
    submitted: bool = False
    approved_by: Optional[str] = None

class TimesheetOut(TimesheetCreate):
    id: int

    class Config:
        orm_mode = True

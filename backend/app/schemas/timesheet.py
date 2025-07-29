from pydantic import BaseModel
from typing import Optional
import datetime

class TimesheetCreate(BaseModel):
    user_id: str
    email: str
    date: datetime.date
    from_time: datetime.time
    to_time: datetime.time
    task_summary: str
    hours: int
    description: str
    submitted: bool = False
    approved_by: Optional[str] = None

class TimesheetOut(TimesheetCreate):
    id: int

    class Config:
        orm_mode = True
        json_encoders = {
            __import__('datetime').date: lambda v: v.isoformat(),
            __import__('datetime').time: lambda v: v.strftime('%H:%M:%S'),
        }

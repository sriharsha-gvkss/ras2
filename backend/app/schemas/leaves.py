from pydantic import BaseModel
from datetime import date
from typing import Optional

class LeaveCreate(BaseModel):
    user_id: str
    email: str
    date: str  # Changed to str since Rasa sends string dates
    leave_type: str
    reason: str
    status: str = "Pending"

class LeaveUpdate(BaseModel):
    status: Optional[str] = None
    approved_by: Optional[str] = None
    approval_comment: Optional[str] = None

class LeaveOut(LeaveCreate):
    id: int
    approved_by: Optional[str] = None
    approval_comment: Optional[str] = None

    class Config:
        orm_mode = True 
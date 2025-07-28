from pydantic import BaseModel
from typing import Optional

class EmailCreate(BaseModel):
    user_id: str
    email: str
    subject: str
    message: str
    type: str = "general"
    status: str = "Unread"

class EmailOut(EmailCreate):
    id: int

    class Config:
        orm_mode = True 
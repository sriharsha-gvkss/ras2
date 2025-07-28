from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    user_id: str
    email: str
    title: str
    description: str
    priority: str = "Medium"
    status: str = "Pending"

class TaskOut(TaskCreate):
    id: int

    class Config:
        orm_mode = True 
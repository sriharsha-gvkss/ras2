from pydantic import BaseModel
from datetime import date

class JobCreate(BaseModel):
    job_title: str
    assigned_to: str
    status: str = "Open"
    start_date: date
    end_date: date
    description: str

class JobOut(JobCreate):
    id: int

    class Config:
        from_attributes = True 
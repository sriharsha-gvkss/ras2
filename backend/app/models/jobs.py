from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title=Column(String)
    assigned_to=Column(String)
    status=Column(String,default="pending")
    start_date=Column(Date)
    end_date=Column(Date)
    description=Column(String)
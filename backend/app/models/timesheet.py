from sqlalchemy import Column,Integer,String,Date,Boolean,Time
from app.database import Base

class Timesheet(Base):
    __tablename__="timesheets"

    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    email = Column(String)
    date = Column(Date)
    from_time = Column(Time) 
    to_time = Column(Time)    
    task_summary = Column(String)  
    hours = Column(Integer)
    description = Column(String)
    submitted = Column(Boolean, default=False)
    approved_by = Column(String, nullable=True)
from sqlalchemy import Column,Integer,String,Date
from app.database import Base

class Task(Base):
    __tablename__="tasks"

    id = Column(Integer,primary_key=True,index=True)
    user_id=Column(String)
    email=Column(String)
    title=Column(String)
    description=Column(String)
    priority=Column(String)
    status=Column(String,default="pending")
    
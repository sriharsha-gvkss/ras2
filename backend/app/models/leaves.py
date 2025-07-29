from sqlalchemy import Column,Integer,String,Date
from app.database import Base 

class Leave(Base):
    __tablename__="leaves"

    id = Column(Integer,primary_key=True,index=True)
    user_id=Column(String)
    email =Column(String)
    date=Column(String)
    leave_type=Column(String)
    reason=Column(String)
    status=Column(String,default="pending")
    approved_by=Column(String,nullable=True)
    approval_comment=Column(String,nullable=True)

from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(String)
    email=Column(String)
    subject=Column(String)
    message=Column(String)
    type=Column(String,default="email")
    status=Column(String,default="unread")
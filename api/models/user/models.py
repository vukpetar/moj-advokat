from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phonenumber = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



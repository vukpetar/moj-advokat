from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String, server_default=None)
    is_admin = Column(Boolean, server_default="false")
    daily_limit = Column(Integer, server_default="2")
    is_activated = Column(Boolean, server_default="false")
    activation_otp_count = Column(Integer, server_default="0")
    activation_code = Column(String, server_default=None)
    hashed_password = Column(String)
    disabled = Column(Boolean)

    questions = relationship("Question")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



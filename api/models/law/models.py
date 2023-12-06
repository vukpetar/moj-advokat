from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from database import Base

class Law(Base):
    __tablename__ = 'laws'
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



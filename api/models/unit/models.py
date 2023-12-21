from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Unit(Base):
    __tablename__ = 'units'
    id  = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    start = Column(Integer)
    end = Column(Integer)
    type = Column(String)

    article = relationship("Article")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

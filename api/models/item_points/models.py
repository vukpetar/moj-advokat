from sqlalchemy import (
    ForeignKey,
    Column,
    DateTime,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class ItemPoint(Base):
    __tablename__ = 'item_points'
    id  = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    text = Column(String)

    article = relationship("Article")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

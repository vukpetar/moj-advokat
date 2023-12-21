from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = 'items'
    id  = Column(Integer, primary_key=True, index=True)
    law_id = Column(Integer, ForeignKey('laws.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))
    start = Column(Integer)
    end = Column(Integer)
    reference = Column(JSONB)

    law = relationship("Law")
    article = relationship("Article")
    question_items = relationship("QuestionItems", back_populates="item")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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

class Article(Base):
    __tablename__ = 'articles'
    id  = Column(Integer, primary_key=True, index=True)
    law_id = Column(Integer, ForeignKey('laws.id'))
    article_title = Column(String)
    article_text = Column(String)

    law = relationship("Law")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

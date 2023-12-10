from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
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
    item_point_ids = Column(JSONB)
    internal_links = Column(JSONB)
    text = Column(String)
    cohere_text = Column(String)

    law = relationship("Law")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

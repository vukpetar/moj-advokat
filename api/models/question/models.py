from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Question(Base):
    __tablename__ = 'questions'
    id  = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    is_public = Column(Boolean, server_default="false")

    user = relationship("User")
    question_items = relationship("QuestionItems", back_populates="question")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class QuestionItems(Base):
    __tablename__ = 'question_items'
    id  = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    distance = Column(Float, server_default=None)

    question = relationship("Question", back_populates="question_items")
    item = relationship("Item")

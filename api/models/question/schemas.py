# build a schema using pydantic
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from models.item.schemas import Item

class QuestionCreate(BaseModel):
    text: str

class Question(QuestionCreate):
    id: int
    user_id: int
    text: str
    is_public: Optional[bool]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class QuestionItems(BaseModel):
    id: int
    question_id: int
    item_id: int
    distance: Optional[float]
    item: Optional[Item]

    class Config:
        orm_mode = True

class QuestionWithItems(Question):
    question_items: List[QuestionItems]

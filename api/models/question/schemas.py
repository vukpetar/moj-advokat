# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class QuestionCreate(BaseModel):
    text: str

class Question(QuestionCreate):
    id: int
    user_id: int
    text: str
    is_public: bool

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
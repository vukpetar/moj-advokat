# build a schema using pydantic
from typing import List, Optional
from pydantic import BaseModel

from models.question.schemas import Question

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str]
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    daily_limit: Optional[int]
    questions: List[Question]

    class Config:
        orm_mode = True
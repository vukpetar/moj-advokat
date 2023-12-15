# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    daily_limit: Optional[int]

    class Config:
        orm_mode = True
# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    first_name: str
    last_name: str
    phonenumber: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    first_name: str
    last_name: str
    email: str
    phonenumber: str
    disabled: Optional[bool] = None

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
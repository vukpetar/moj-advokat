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
    phone_number: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: Optional[bool] = None
    is_admin: Optional[bool]
    daily_limit: Optional[int]
    is_activated: bool
    activation_code: str

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
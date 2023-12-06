# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class LawCreate(BaseModel):
    title: str

class Law(LawCreate):
    id: int
    title: str

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
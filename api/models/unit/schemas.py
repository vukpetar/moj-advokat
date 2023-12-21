# build a schema using pydantic
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime

class UnitCreate(BaseModel):
    article_id: int
    start: int
    end: int
    type: str

class Unit(UnitCreate):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
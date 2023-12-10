# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ItemPointCreate(BaseModel):
    article_id: int
    text: str

class ItemPoint(ItemPointCreate):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
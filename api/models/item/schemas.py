# build a schema using pydantic
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime

class ItemCreate(BaseModel):
    law_id: int
    item_point_ids: List[int]
    internal_links: List[Dict]
    text: str
    cohere_text: str

class Item(ItemCreate):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
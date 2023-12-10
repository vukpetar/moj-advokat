# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ArticleCreate(BaseModel):
    law_id: int
    article_title: str
    article_group: Optional[str]

class Article(ArticleCreate):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
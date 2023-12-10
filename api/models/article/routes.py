from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.article import (
    crud as articleCrud,
    schemas as articleSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from models.user.schemas import User
from database import get_db

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=articleSchemas.Article)
def create_article(article: articleSchemas.ArticleCreate, db: Session = Depends(get_db)):

    return articleCrud.create_article(db=db, article=article)

@router.get("/", response_model=list[articleSchemas.Article])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    articles = articleCrud.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/{article_id}", response_model=articleSchemas.Article)
def read_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_article = articleCrud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article
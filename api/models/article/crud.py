from sqlalchemy.orm import Session

from models.article import (
    models,
    schemas
)

def get_article(db: Session, article_id: int) -> schemas.Article:

    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.Article):
    
    db_article = models.Article(
        law_id = article.law_id,
        article_group = article.article_group,
        article_title = article.article_title,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

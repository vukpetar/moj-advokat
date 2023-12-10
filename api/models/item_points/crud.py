from sqlalchemy.orm import Session

from models.item_points import (
    models,
    schemas
)

def get_item_point(db: Session, item_point_id: int) -> schemas.ItemPoint:

    return db.query(models.ItemPoint).filter(models.ItemPoint.id == item_point_id).first()

def get_item_points(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.ItemPoint).offset(skip).limit(limit).all()


def create_item_point(db: Session, item_point: schemas.ItemPoint):
    
    db_item_point = models.ItemPoint(
        article_id = item_point.article_id,
        text = item_point.text
    )
    db.add(db_item_point)
    db.commit()
    db.refresh(db_item_point)
    return db_item_point

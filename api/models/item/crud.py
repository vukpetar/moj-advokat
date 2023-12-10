from sqlalchemy.orm import Session

from models.item import (
    models,
    schemas
)

def get_item(db: Session, item_id: int) -> schemas.Item:

    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.Item):
    
    db_item = models.Item(
        law_id = item.law_id,
        item_point_ids = item.item_point_ids,
        internal_links = item.internal_links,
        text = item.text,
        cohere_text = item.cohere_text,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

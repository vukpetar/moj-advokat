from sqlalchemy.orm import Session

from models.unit import (
    models,
    schemas
)

def get_unit(db: Session, unit_id: int) -> schemas.Unit:

    return db.query(models.Unit).filter(models.Unit.id == unit_id).first()

def get_units(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Unit).offset(skip).limit(limit).all()


def create_unit(db: Session, unit: schemas.Unit):
    
    db_unit = models.Unit(
        article_id = unit.article_id,
        start = unit.start,
        end = unit.end,
        type = unit.type,
    )
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

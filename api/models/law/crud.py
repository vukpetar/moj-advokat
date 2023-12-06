from sqlalchemy.orm import Session

from models.law import (
    models,
    schemas
)

def get_law(db: Session, law_id: int) -> schemas.Law:

    return db.query(models.Law).filter(models.Law.id == law_id).first()

def get_laws(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Law).offset(skip).limit(limit).all()


def create_law(db: Session, law: schemas.Law):
    
    db_law = models.Law(
        title = law.title,
    )
    db.add(db_law)
    db.commit()
    db.refresh(db_law)
    return db_law

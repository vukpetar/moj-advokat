from sqlalchemy.orm import Session

from models.user import (
    models,
    schemas
)

def get_user(db: Session, user_id: int) -> schemas.User:

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    
    from models.user.auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        phonenumber = user.phonenumber,
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

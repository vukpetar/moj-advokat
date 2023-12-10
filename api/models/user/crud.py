from sqlalchemy.orm import Session
from random import randint

from models.user import (
    models,
    schemas
)
from mailgun import send_email

def get_user(db: Session, user_id: int) -> schemas.User:

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    
    from models.user.auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    activation_code = randint(1000, 9999)
    db_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        phone_number = user.phone_number,
        email = user.email,
        hashed_password = hashed_password,
        activation_code=activation_code
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    send_email(
        subject = "MojAdvokat Aktivacioni Kod",
        message = f"Vaš aktivacioni kod je: {activation_code}",
        to = [user.email]
    )

    return db_user

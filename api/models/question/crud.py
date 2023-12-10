from sqlalchemy.orm import Session

from models.question import (
    models,
    schemas
)
from models.user.schemas import User

def get_question(db: Session, question_id: int) -> schemas.Question:

    return db.query(models.Question).filter(models.Question.id == question_id).first()

def get_questions(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Question).offset(skip).limit(limit).all()


def create_question(
        db: Session,
        question: schemas.Question,
        current_user: User
    ):
    

    db_question = models.Question(
        user_id = current_user.id,
        text = question.text
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

from fastapi import HTTPException, status
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
    
    if current_user.daily_limit == 0:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You have exceeded the daily limit.")
    
    current_user.daily_limit -= 1
    db_question = models.Question(
        user_id = current_user.id,
        text = question.text
    )
    db.add(db_question)
    db.add(current_user)
    db.commit()
    db.refresh(db_question)
    db.refresh(current_user)    

    return db_question

def get_question_item(db: Session, question_id: int):

    return db.query(models.QuestionItems).filter(models.QuestionItems.question_id == question_id).first()

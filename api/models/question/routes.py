from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.question import (
    crud as questionCrud,
    schemas as questionSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from models.user.schemas import User
from database import get_db

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=questionSchemas.Question)
def create_question(
    question: questionSchemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):

    return questionCrud.create_question(db=db, question=question, current_user=current_user)

@router.get("/", response_model=list[questionSchemas.Question])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    questions = questionCrud.get_questions(db, skip=skip, limit=limit)
    return questions

@router.get("/{question_id}", response_model=questionSchemas.Question)
def read_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_question = questionCrud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_question
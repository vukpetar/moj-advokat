import os
from dotenv import load_dotenv
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.question import (
    crud as questionCrud,
    schemas as questionSchemas,
    models as questionModels
)
from models.user.auth import (
    get_current_active_user,
)
from models.user.schemas import User
from database import get_db

import cohere
import pinecone

load_dotenv('.env')

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=questionSchemas.QuestionWithItems)
async def create_question(
    question: questionSchemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_question = questionCrud.create_question(db=db, question=question, current_user=current_user)
    co = cohere.Client(os.environ["COHERE_KEY"])
    pinecone.init(api_key=os.environ["PINECONE_KEY"], environment=os.environ["PINECONE_ENV"]) 
    index = pinecone.Index(os.environ["PINECONE_INDEX"])
    query_embed = co.embed(
        texts=[question.text],
        model="embed-multilingual-v3.0",
        input_type="search_document"
    ).embeddings
    query_response = index.query(
        namespace=os.environ["PINECONE_NAMESPACE"],
        top_k=10,
        include_metadata=True,
        vector=query_embed[0],
    )

    db_question_items = []
    for match in query_response["matches"]:
        db_question_item = questionModels.QuestionItems(
            question_id = db_question.id,
            item_id = match["id"],
            distance = match["score"]
        )
        db.add(db_question_item)
        db_question_items.append(db_question_item)

    db.commit()
    db.refresh(db_question)
    
    return db_question

@router.get("/", response_model=list[questionSchemas.Question])
async def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    questions = questionCrud.get_questions(db, skip=skip, limit=limit)
    return questions

@router.get("/{question_id}", response_model=questionSchemas.QuestionWithItems)
async def read_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_question = questionCrud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.get("/{question_id}/items", response_model=questionSchemas.QuestionItems)
async def read_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    
    db_question = questionCrud.get_question_item(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.law import (
    crud as lawCrud,
    schemas as lawSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from database import get_db

router = APIRouter(
    prefix="/laws",
    tags=["laws"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=lawSchemas.Law)
def create_law(law: lawSchemas.LawCreate, db: Session = Depends(get_db)):

    return lawCrud.create_law(db=db, law=law)

@router.get("/", response_model=list[lawSchemas.Law])
def read_laws(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    laws = lawCrud.get_laws(db, skip=skip, limit=limit)
    return laws

@router.get("/{law_id}", response_model=lawSchemas.Law)
def read_law(
    law_id: int,
    db: Session = Depends(get_db),
    current_user: lawSchemas.Law = Depends(get_current_active_user)
):
    
    db_law = lawCrud.get_law(db, law_id=law_id)
    if db_law is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_law
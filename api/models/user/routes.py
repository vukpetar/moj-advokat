from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user import (
    crud as userCrud,
    schemas as userSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/users/", response_model=userSchemas.User)
async def create_user(user: userSchemas.UserCreate, db: Session = Depends(get_db)):

    db_user = userCrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return userCrud.create_user(db=db, user=user)

@router.get("/users/", response_model=list[userSchemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    users = userCrud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=userSchemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: userSchemas.User = Depends(get_current_active_user)
):
    
    db_user = userCrud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
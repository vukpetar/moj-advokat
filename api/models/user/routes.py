from datetime import timedelta
import os
from typing import Annotated
from dotenv import load_dotenv
from random import randint

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from models.user import (
    crud as userCrud,
    schemas as userSchemas
)
from models.user.auth import (
    create_access_token,
    get_current_active_user,
)
from database import get_db
from mailgun import send_email

load_dotenv('.env')

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=userSchemas.User)
async def create_user(user: userSchemas.UserCreate, db: Session = Depends(get_db)):

    db_user = userCrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return userCrud.create_user(db=db, user=user)

@router.get("/", response_model=list[userSchemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    users = userCrud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=userSchemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: userSchemas.User = Depends(get_current_active_user)
):
    
    db_user = userCrud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/activate", response_model=userSchemas.Token)
async def activate_user(
    email: Annotated[str, Form()],
    activation_code: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    
    db_user = userCrud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already active")
    if db_user.activation_code != activation_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The activation code is not valid")
    else:
        db_user.activation_code = None
        db_user.is_activated = True
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    access_token_expires = timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    result = userSchemas.Token(access_token = access_token, token_type = "bearer")
    
    return result

@router.post("/resend_activation_code")
async def resend_activation_code(
    email: str,
    db: Session = Depends(get_db)
):
    
    db_user = userCrud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already active")
    
    max_otp_count = int(os.getenv("MAX_OTP_COUNT", 5))
    if db_user.activation_otp_count >= max_otp_count:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have exceeded the limit of sent OTP codes")
    else:
        activation_code = randint(1000, 9999)
        db_user.activation_code = activation_code
        db_user.activation_otp_count += 1
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        send_email(
            subject = "MojAdvokat Aktivacioni Kod",
            message = f"Vaš aktivacioni kod je: {activation_code}",
            to = [db_user.email]
        )

    return True
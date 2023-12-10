import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from models.user import (
    schemas as userSchemas
)
from models.user.crud import (
    get_user,
    get_user_by_email
)
from database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv('.env')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(
        email: int,
        password: str,
        db: Session = Depends(get_db)
    ) -> userSchemas.User or bool:
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credential_exception
        
    except JWTError as e:
        raise credential_exception

    user = get_user(db, user_id=user_id)
    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(current_user: userSchemas.User = Depends(get_current_user)):

    if current_user.disabled or not current_user.is_activated:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

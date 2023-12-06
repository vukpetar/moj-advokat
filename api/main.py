import os
from dotenv import load_dotenv
from datetime import timedelta

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from models.user import (
    crud as userCrud,
    schemas as userSchemas
)
from models.user.auth import (
    authenticate_user,
    create_access_token
)
from models.user.auth import (
    get_current_active_user,
)
from models.law import (
    crud as lawCrud,
    schemas as lawSchemas
)
from database import get_db

load_dotenv('.env')
app = FastAPI()

@app.post("/token", response_model=userSchemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=userSchemas.User)
def create_user(user: userSchemas.UserCreate, db: Session = Depends(get_db)):

    db_user = userCrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return userCrud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[userSchemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    users = userCrud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=userSchemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: userSchemas.User = Depends(get_current_active_user)
):
    
    db_user = userCrud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/laws/", response_model=lawSchemas.Law)
def create_law(law: lawSchemas.LawCreate, db: Session = Depends(get_db)):

    return lawCrud.create_law(db=db, law=law)

@app.get("/laws/", response_model=list[lawSchemas.Law])
def read_laws(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    laws = lawCrud.get_laws(db, skip=skip, limit=limit)
    return laws

@app.get("/laws/{law_id}", response_model=lawSchemas.Law)
def read_law(
    law_id: int,
    db: Session = Depends(get_db),
    current_user: lawSchemas.Law = Depends(get_current_active_user)
):
    
    db_law = lawCrud.get_law(db, law_id=law_id)
    if db_law is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_law

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

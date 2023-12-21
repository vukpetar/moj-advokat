import os
from dotenv import load_dotenv
from datetime import timedelta

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models.user.routes as userRoutes
import models.law.routes as lawRoutes
import models.article.routes as articleRoutes
import models.item.routes as itemRoutes
import models.unit.routes as unitRoutes
import models.question.routes as questionRoutes
from models.user import (
    schemas as userSchemas
)
from models.user.auth import (
    authenticate_user,
    create_access_token
)
from database import get_db

load_dotenv('.env')
app = FastAPI()
app.include_router(userRoutes.router)
app.include_router(lawRoutes.router)
app.include_router(articleRoutes.router)
app.include_router(itemRoutes.router)
app.include_router(questionRoutes.router)
app.include_router(unitRoutes.router)

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

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..database import  get_db

router = APIRouter(tags=["Authenticztion"])

@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    userFromDB = db.query(models.User).filter(models.User.email == user.username).first()
    if userFromDB is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with email {user.username} not found")
    if utils.verify(user.password, userFromDB.password) is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid password")
    token = oauth2.create_access_token(data={"uid": userFromDB.id})
    return {"access_token": token, "token_type": "bearer"}
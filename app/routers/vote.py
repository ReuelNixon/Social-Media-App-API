from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import  get_db

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.get("/", response_model=List[schemas.VoteResponse])
def get_all_votes(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    votes = db.query(models.Vote).all()
    return votes

@router.get("/post/{pid}", response_model=List[schemas.VoteResponse])
def get_votes_by_pid(pid: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == pid).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {pid} not found")
    votes = db.query(models.Vote).filter(models.Vote.pid == pid).all()
    return votes

@router.get("/user/{uid}", response_model=List[schemas.VoteResponse])
def get_votes_by_uid(uid: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == uid).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {uid} not found")
    votes = db.query(models.Vote).filter(models.Vote.uid == uid).all()
    return votes

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteRequest, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.pid).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.pid} not found")
    
    voteInDB = db.query(models.Vote).filter(models.Vote.uid == current_user.id, models.Vote.pid == vote.pid).first()
    if vote.up == True:
        if voteInDB is None:
            new_vote = models.Vote(pid=vote.pid, uid=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {
                "message": "Vote successful",
                "detail": f"User with id {current_user.id} voted on post with id {vote.pid}"
                }
        
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with id {current_user.id} already voted on post with id {vote.pid}")
    else:
        if voteInDB is not None:
            db.delete(voteInDB)
            db.commit()
            return {
                "message": "Down-vote successful",
                "detail": f"User with id {current_user.id} down-voted on post with id {vote.pid}"
                }
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id {current_user.id} has not voted on post with id {vote.pid}")

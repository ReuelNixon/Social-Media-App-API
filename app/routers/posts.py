from typing import List
from fastapi import Depends, APIRouter, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostResponse])
def getPosts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # return {'data': cursor.fetchall()}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPost(post: schemas.PostRequest, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # cursor.execute(f"INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.is_published))
    # conn.commit()
    # return {'data': cursor.fetchone()}


@router.get("/{id}", response_model=schemas.PostResponse)
def getPost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post

    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    # if post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id {id} not found")
    # return {'data':post}


@router.put("/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.PostRequest, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    postFromDB = postQuery.first()
    if postFromDB is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    postQuery.update(post.dict())
    db.commit()
    return postQuery.first()

    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # postFromDB = cursor.fetchone()
    # if postFromDB is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id {id} not found")
    # cursor.execute("UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.is_published, str(id)))
    # conn.commit()
    # return cursor.fetchone()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    # cursor.execute("DELETE FROM posts WHERE id = %s", (str(id)))
    # conn.commit()
    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id {id} not found")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

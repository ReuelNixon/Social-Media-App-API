from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True

@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/posts")
def getPosts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts}

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # return {'data': cursor.fetchall()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}

    # cursor.execute(f"INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.is_published))
    # conn.commit()
    # return {'data': cursor.fetchone()}


@app.get("/posts/{id}")
def getPost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {'data':post}

    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    # if post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id {id} not found")
    # return {'data':post}


@app.put("/posts/{id}")
def updatePost(id: int, post: Post, db: Session = Depends(get_db)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    postFromDB = postQuery.first()
    if postFromDB is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    postQuery.update(post.dict())
    db.commit()
    return {'data': postQuery.first()}

    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # postFromDB = cursor.fetchone()
    # if postFromDB is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id {id} not found")
    # cursor.execute("UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.is_published, str(id)))
    # conn.commit()
    # return cursor.fetchone()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db)):
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
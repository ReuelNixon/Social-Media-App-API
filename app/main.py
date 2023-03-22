from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def getPosts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # return {'data': cursor.fetchall()}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPost(post: schemas.PostRequest, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # cursor.execute(f"INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.is_published))
    # conn.commit()
    # return {'data': cursor.fetchone()}


@app.get("/posts/{id}", response_model=schemas.PostResponse)
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


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.PostRequest, db: Session = Depends(get_db)):
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




@app.get("/users", response_model=List[schemas.UserResponse])
def getUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def createUser(user: schemas.UserRequest, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user


@app.put("/users/{id}", response_model=schemas.UserResponse)
def updateUser(id: int, user: schemas.UserRequest, db: Session = Depends(get_db)):
    userQuery = db.query(models.User).filter(models.User.id == id)
    userFromDB = userQuery.first()
    if userFromDB is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    userQuery.update(user.dict())
    db.commit()
    return userQuery.first()


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
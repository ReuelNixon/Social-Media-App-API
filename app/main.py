import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'FastAPI', user='postgres', password='thanimai', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to database")
        break
    except Exception as e:
        print("Error while connecting to database\n", e)
        time.sleep(2)

@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/posts")
def getPosts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    if post.is_published:
        cursor.execute(f"INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.is_published))
    else:
        cursor.execute(f"INSERT INTO posts (title, content) VALUES ('%s', '%s') RETURNING *", (post.title, post.content))
    conn.commit()
    return cursor.fetchone()


@app.get("/posts/{id}")
def getPost(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    postFromDB = cursor.fetchone()
    if postFromDB is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    if post.is_published:
        cursor.execute("UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.is_published, str(id)))
    else:
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (post.title, post.content, str(id)))
    conn.commit()
    return cursor.fetchone()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (str(id)))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
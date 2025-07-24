from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import get_db, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='balaji', 
            password='balaji',
            cursor_factory=RealDictCursor
        )
        cursor=conn.cursor()
        print('database connection successfull')
        break
    except Exception as error:
        print(f'database conenction error: {error}')
        time.sleep(2)

my_posts = [
        {
            'title': 'top beaches in chenn',
            'id': 1, 
            'content': 'Checkout these awesome beaches', 
            'published': True, 
            'rating': 5
        }, 
        {
            'title': 'top beaches in chennai', 
            'id': 2, 
            'content': 'Checkout these awesome beaches', 
            'published': True, 
            'rating': 5
        }
    ]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
def hello() -> dict:
    return {
        "message" : "Hello World!"
    }

@app.get('/posts')
# def get_posts() -> dict:
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}
async def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}

# @app.get('/sql')
# async def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post, db: Session = Depends(get_db)) :
    created_post = models.Post(**new_post.model_dump())
    # print(created_post)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return {
        'data': created_post
    }

@app.get('/post/{id}')
def get_post(id) -> dict:
    cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found')
    return{
        'post_detail': f'this is the post of the {post}'
    }

@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = (%s) RETURNING *""", str((id)))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found'
                        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/post/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post) -> dict:
        cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
        updated_post = cursor.fetchone()
        conn.commit()
        if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found'
                        )
        return{
            'update_status': f"The post with id: {id} is updated with {updated_post}"
        }

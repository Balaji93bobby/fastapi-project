from random import randrange
from turtle import pos
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
def get_posts() -> dict:
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post) -> dict:
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {
        'message': 'post created successfully', 
        "all_posts": my_posts
    }

@app.get('/post/{id}')
def get_post(id: int) -> dict:
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found')
    return{
        'post_detail': f'this is the post of the {post}'
    }

@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found'
                        )
    else:
        my_posts.remove(post)


@app.put('/post/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post) -> dict:
        index = find_index_post(id)
        if index == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'psot with id : {id} not does not exist'
                )
        post_dict = post.model_dump()
        post_dict['id']  = id  
        my_posts[index] = post_dict
        return{
            'update_status': f"The post with id: {id} is updated with {post}"
        }
from ast import Dict
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

class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True



@app.get('/')
def hello() -> dict:
    return {
        "message" : "Hello World!"
    }



@app.get('/posts')
async def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}



@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(new_post: PostSchema, db: Session = Depends(get_db)) :
    created_post = models.Post(**new_post.model_dump())
    # print(created_post)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return {
        'data': created_post
    }

@app.get('/post/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the requested post for the id: {id} is not found")
    return{
            'post_detail': f'this is the post of the {id}',
            'data': post
        }

@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found'
                        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/post/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: PostSchema, db: Session = Depends(get_db)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query_post.first()

    if existing_post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    query_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return {
        "update_status": f"The post with id: {id} is updated",
        "data": query_post.first()  # returns the updated object
    }

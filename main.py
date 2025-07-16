from struct import pack
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
def hello() -> dict:
    return {"message" : "Hello World!"}

@app.get('/posts')
def post() -> dict:
    return {'data': 'this is the post'}

@app.post('/createposts')
def create_posts(new_post: Post) -> dict:
    print(new_post)
    return {'message': 'post created successfully', "post": new_post}


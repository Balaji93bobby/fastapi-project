from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from . import models, utils
from .schemas import AllPosts, CreateUser, CreatePost, UpdatePost, ResponsePost, User, UserDetail
from .database import get_db, engine
from sqlalchemy.orm import Session
from typing import List



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def hello() -> dict:
    return {
        "message" : "Hello World!"
    }



@app.get('/posts', response_model=List[AllPosts])
async def test(db: Session = Depends(get_db)) :
    posts = db.query(models.Post).all()
    return posts



@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
def create_post(new_post: CreatePost, db: Session = Depends(get_db)) :
    created_post = models.Post(**new_post.model_dump())
    # print(created_post)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@app.get('/post/{id}', response_model=ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the requested post for the id: {id} is not found")
    return post

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

@app.put('/post/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ResponsePost)
def update_post(id: int, post: UpdatePost, db: Session = Depends(get_db)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query_post.first()

    if existing_post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    query_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return  query_post.first()  # returns the updated object
    
@app.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=UserDetail)
def create_user(new_user: CreateUser, db: Session = Depends(get_db)):

    #hashing the password

    hashed_password = utils.hash(new_user.password)

    new_user.password = hashed_password

    # user_list = db.query(models.User).all()
    created_user = models.User(**new_user.model_dump())
    # for user in user_list:
    #     print(type(user))
    #     if created_user.email in user.items('email'):
    #         return{
    #             'error': 'user already created,please login'
    #         }
    #     break        
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[UserDetail])
def get_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()
    return user_list

@app.get('/users/{id}', response_model=UserDetail)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the user with id: {id} does not exist"
                            )
    return user
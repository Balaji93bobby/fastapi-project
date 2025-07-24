from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter, FastAPI, Response
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router =  APIRouter(
    prefix='/post',
    tags=['Posts']
)



@router.get('/', response_model=List[schemas.AllPosts])
async def test(db: Session = Depends(get_db)) :
    posts = db.query(models.Post).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(new_post: schemas.CreatePost, db: Session = Depends(get_db)) :
    created_post = models.Post(**new_post.model_dump())
    # print(created_post)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@router.get('/{id}', response_model=schemas.ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the requested post for the id: {id} is not found")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id: {id} is not found'
                        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query_post.first()

    if existing_post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    query_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return  query_post.first()  # returns the updated object
    
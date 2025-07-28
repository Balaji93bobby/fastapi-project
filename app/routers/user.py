from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router =  APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserDetail)
def create_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    created_user = models.User(**new_user.model_dump())      
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserDetail])
def get_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()
    return user_list

@router.get('/{id}', response_model=schemas.UserDetail)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the user with id: {id} does not exist"
                            )
    return user
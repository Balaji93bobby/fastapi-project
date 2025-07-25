import stat
from fastapi import APIRouter , Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from .. import schemas, database, models, utils


router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(user_creds: schemas.UserLogin,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid Credentials')
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid Credentials')
    return {'token': 'example token'}
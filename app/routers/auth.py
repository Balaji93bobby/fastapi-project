from fastapi import APIRouter , Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(user_creds: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')
    
    access_token  = oauth2.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token,
            'token_type': 'bearer'
            }



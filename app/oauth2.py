from time import timezone
from jose import JWTError, jwt
from datetime import UTC, datetime, timedelta, timezone
from .schemas import TokenData, Token
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '066af464d74e74df59770474aeba0751279d4bf0da29ced6491b8d4fc8b6a3ef'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get('user_id')

        if id is None:
            raise credentials_exception
    
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"could not validate credentials",
                                        headers={'WWW-Authenticate': 'Bearer'}
                                        )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
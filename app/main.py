from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

from app.routers import auth
from .database import get_db, engine
from sqlalchemy.orm import Session
from typing import List
from . import models
from .routers import post, user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def hello() -> dict:
    return {
        "message" : "Hello World!"
    }


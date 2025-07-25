from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(Post):
    pass


class UpdatePost(Post):
    pass


class ResponsePost(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AllPosts(Post):
    pass
    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User):
    pass

class UserDetail(BaseModel):
    id: int
    email: str
    created_at: datetime
    pass
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
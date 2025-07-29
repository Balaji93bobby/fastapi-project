from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional

from sqlalchemy import Boolean

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(Post):
    pass


class UpdatePost(Post):
    pass


# class ResponsePost(Post):
#     id: int
#     created_at: datetime
#     user_id: int
    

#     class Config:
#         from_attributes = True

class AllPosts(Post):
    id: int
    created_at: datetime
    user_id: int
    class Config:
        from_attributes = True

class User(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User):
    pass

class UserDetail(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class ResponsePost(Post):
    id: int
    created_at: datetime
    user_id: int
    user: UserDetail
    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
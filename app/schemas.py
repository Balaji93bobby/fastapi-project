from datetime import datetime
from click import DateTime
from pydantic import BaseModel

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
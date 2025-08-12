from fastapi import Body, FastAPI
# from app.routers import auth
# from .database import engine
# from . import models
from .routers import post, user, vote, auth
# from .config import settings


# models.Base.metadata.create_all(bind=engine) this si used to create ak the tables at the start of the applicaiton
# since we use alembic now there is no need for the above.


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



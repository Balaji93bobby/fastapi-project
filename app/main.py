from fastapi import Body, FastAPI
# from app.routers import auth
# from .database import engine
# from . import models
from .routers import post, user, vote, auth
# from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) this si used to create ak the tables at the start of the applicaiton
# since we use alembic now there is no need for the above.


app = FastAPI()
origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*']
)

@app.get('/')
def Hello():
    return {'hello': 'world'}
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



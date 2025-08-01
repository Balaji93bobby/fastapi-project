from fastapi import Body, FastAPI
from app.routers import auth
from .database import engine
from . import models
from .routers import post, user, vote
from .config import settings
import os
from prometheus_fastapi_instrumentator import Instrumentator

models.Base.metadata.create_all(bind=engine)
os.environ["ENABLE_METRICS"] = settings.enable_metrics
app = FastAPI()

# Instrumentation setup
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    excluded_handlers=["/metrics"],  # Avoid recursive scrape
    env_var_name="ENABLE_METRICS"
)
instrumentator.instrument(app).expose(app, endpoint="/metrics")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

app.include_router(vote.router)



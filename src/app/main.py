from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.database import create_db_and_tables
from src.app.routers import (
    project_tag,
    users,
    tag,
    activity,
    challenge_match,
    comment,
    project,
    user_tag,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(tag.router)
app.include_router(activity.router)
app.include_router(challenge_match.router)
app.include_router(comment.router)
app.include_router(project.router)
app.include_router(project_tag.router)
app.include_router(user_tag.router)

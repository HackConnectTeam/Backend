from contextlib import asynccontextmanager

from src.app.config.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.database import create_db_and_tables
from src.app.routers import (
    project_tag,
    users,
    tag,
    activity,
    challenge_match,
    # comment,
    project,
    user_tag,
    model,
    check_activity,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        settings.frontend.url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tag.router)
app.include_router(activity.router)
app.include_router(challenge_match.router)
# app.include_router(comment.router)
app.include_router(project.router)
app.include_router(project_tag.router)
app.include_router(user_tag.router)
app.include_router(model.router)

app.include_router(check_activity.router)

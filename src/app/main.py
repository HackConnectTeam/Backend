from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.database import create_db_and_tables
from src.app.routers import (
    post,
    project_tag,
    users,
    tag,
    activity,
    project,
    user_tag,
    model,
    check_activity,
    generate_names,
    country,
    team,
    image_retrieval,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tag.router)
app.include_router(activity.router)
app.include_router(post.router)
# app.include_router(comment.router)
app.include_router(project.router)
app.include_router(project_tag.router)
app.include_router(user_tag.router)
app.include_router(model.router)
app.include_router(team.router)

app.include_router(check_activity.router)
app.include_router(generate_names.router)
app.include_router(country.router)

app.include_router(team.router)
app.include_router(image_retrieval.router)

from contextlib import asynccontextmanager

from common.utils.db_utils import get_db_uri
from fastapi import FastAPI, Body, Depends, BackgroundTasks, APIRouter
from fastapi.openapi.utils import get_openapi
from scripts.init_db import init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(get_db_uri())
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(drop_existing=True)
    yield

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
app = FastAPI(docs_url="/api/docs",
              openapi_url="/api/openapi.json",
              prefix="/api",
              lifespan=lifespan)
app.include_router(router, prefix="/api")
@app.post(
    "/api/fun",
    tags=["Prueba"],
    summary="",
    description="""
    """
)
async def predict(
    background_tasks: BackgroundTasks,
    db = Depends(get_db),
):
    pass


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Inference API",
        version="1.0.0",
        description="Dummy API.",
        routes=app.routes
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
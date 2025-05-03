from typing import Annotated, List
from fastapi import APIRouter, Query

from src.app.crud.project_tag import project_tag as crud_project_tag
from src.app.database import SessionDep
from src.app.models.user_tag import UserTag

router = APIRouter(prefix="/project_tag", tags=["project_tag"])


@router.get("/", response_model=List[UserTag])
def read_project_tags(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_project_tag.get_all(db=session, offset=offset, limit=limit)

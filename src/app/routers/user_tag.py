from typing import Annotated, List
from fastapi import APIRouter, Query

from src.app.crud.user_tag import user_tag as crud_user_tag
from src.app.database import SessionDep
from src.app.models.user_tag import UserTag

router = APIRouter(prefix="/user_tag", tags=["user_tag"])


@router.get("/", response_model=List[UserTag])
def read_user_tags(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_user_tag.get_all(db=session, offset=offset, limit=limit)


@router.get("/user_tags/{user_id}", response_model=List[UserTag])
def read_user_tags_by_id(
    user_id: str,
    session: SessionDep,
):
    """
    Retrieves UserTag entries for a specific user ID.
    """
    return crud_user_tag.get_by_field(db=session, field_name="user_id", value=user_id)

from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query

from src.app.crud.tag import tag as crud_tag
from src.app.database import SessionDep
from src.app.models.tag import TagCreate, TagPublic

router = APIRouter(prefix="/tag", tags=["tag"])


@router.get("/", response_model=List[TagPublic])
def read_tags(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_tag.get_all(db=session, offset=offset, limit=limit)


@router.get("/{tag_id}", response_model=TagPublic)
def read_tag(tag_id: int, session: SessionDep):
    db_tag = crud_tag.get(db=session, id=tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.post("/", response_model=TagPublic)
def create_tag(tag: TagCreate, session: SessionDep):
    return crud_tag.create(db=session, obj_in=tag)


@router.delete("/{tag_id}", response_model=TagPublic)
def delete_tag(tag_id: int, session: SessionDep):
    db_tag = crud_tag.delete(db=session, id=tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

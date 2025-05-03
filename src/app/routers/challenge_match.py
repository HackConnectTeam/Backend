from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query

from src.app.crud.post import post as crud_post
from src.app.database import SessionDep
from src.app.models.post import (
    PostPublic,
    PostCreate,
    PostUpdate,
)

router = APIRouter(prefix="/post", tags=["post"])


@router.get("/", response_model=List[PostPublic])
def read_postes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_post.get_all(db=session, offset=offset, limit=limit)


@router.get("/{post_id}", response_model=PostPublic)
def read_post(post_id: int, session: SessionDep):
    db_post = crud_post.get(db=session, id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Challenge Match not found")
    return db_post


@router.post("/", response_model=PostPublic)
def create_post(post: PostCreate, session: SessionDep):
    return crud_post.create(db=session, obj_in=post)


@router.put("/{post_id}", response_model=PostPublic)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    session: SessionDep,
):
    db_post = crud_post.get(db=session, id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Challenge Match not found")
    return crud_post.update(db=session, db_obj=db_post, obj_in=post_update)


@router.delete("/{post_id}", response_model=PostPublic)
def delete_post(post_id: int, session: SessionDep):
    db_post = crud_post.delete(db=session, id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Challenge Match not found")
    return db_post

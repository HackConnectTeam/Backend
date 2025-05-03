from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query

from src.app.crud.comment import comment as crud_comment
from src.app.database import SessionDep
from src.app.models.comment import CommentCreate, CommentPublic, CommentUpdate

router = APIRouter(prefix="/comment", tags=["comment"])


@router.get("/", response_model=List[CommentPublic])
def read_comments(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_comment.get_all(db=session, offset=offset, limit=limit)


@router.get("/{comment_id}", response_model=CommentPublic)
def read_comment(comment_id: int, session: SessionDep):
    db_comment = crud_comment.get(db=session, id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.post("/", response_model=CommentPublic)
def create_comment(comment: CommentCreate, session: SessionDep):
    return crud_comment.create(db=session, obj_in=comment)


@router.put("/{comment_id}", response_model=CommentPublic)
def update_comment(comment_id: int, comment_update: CommentUpdate, session: SessionDep):
    db_comment = crud_comment.get(db=session, id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return crud_comment.update(db=session, db_obj=db_comment, obj_in=comment_update)


@router.delete("/{comment_id}", response_model=CommentPublic)
def delete_comment(comment_id: int, session: SessionDep):
    db_comment = crud_comment.delete(db=session, id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

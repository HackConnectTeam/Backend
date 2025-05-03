from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from src.app.crud.activity import activity as crud_activity
from src.app.crud.tag import tag as crud_tag
from src.app.database import SessionDep
from src.app.models.activity import (
    Activity,
    ActivityCreate,
    ActivityPublic,
    ActivityUpdate,
)
from src.app.models.tag import Tag

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/", response_model=List[ActivityPublic])
def read_activities(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_activity.get_all(db=session, offset=offset, limit=limit)


@router.get("/{activity_id}", response_model=ActivityPublic)
def read_activity(activity_id: int, session: SessionDep):
    db_activity = crud_activity.get(db=session, id=activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity


@router.post("/", response_model=ActivityPublic)
def create_activity(activity: ActivityCreate, session: SessionDep):
    tag = session.exec(select(Tag).where(Tag.name == activity.tag)).first()

    if not tag:
        tag = crud_tag.create(db=session, obj_in=Tag(name=activity.tag))

    return crud_activity.create(
        db=session,
        obj_in=Activity(
            description=activity.description,
            event_type=activity.event_type,
            points=activity.points,
            tag_id=tag.id,
        ),
    )


@router.put("/{activity_id}", response_model=ActivityPublic)
def update_activity(
    activity_id: int, activity_update: ActivityUpdate, session: SessionDep
):
    db_activity = crud_activity.get(db=session, id=activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="activity not found")
    return crud_activity.update(db=session, db_obj=db_activity, obj_in=activity_update)


@router.delete("/{activity_id}", response_model=ActivityPublic)
def delete_tag(activity_id: int, session: SessionDep):
    db_activity = crud_activity.delete(db=session, id=activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from src.app.crud.user import user as crud_user
from src.app.crud.tag import tag as crud_tag
from src.app.crud.user_tag import user_tag as crud_user_tag
from src.app.crud.activity import activity as crud_activity
from src.app.crud.post import post as crud_post
from src.app.database import SessionDep
from src.app.models.post import Post, PostCreate
from src.app.models.tag import Tag
from src.app.models.user import UsersCreate, UsersUpdate, UsersPublic
from src.app.models.user_tag import UserTag

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UsersPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_user.get_all(db=session, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UsersPublic)
def read_user(user_id: str, session: SessionDep):
    db_user = crud_user.get(db=session, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/exists/{user_id}")
def user_exists(user_id: str, session: SessionDep):
    exists = crud_user.get(db=session, id=user_id) is not None
    return {"exists": exists}


@router.post("/", response_model=UsersPublic)
def create_user(user: UsersCreate, session: SessionDep):
    return crud_user.create(db=session, obj_in=user)


@router.patch("/{user_id}", response_model=UsersPublic)
def update_user(user_id: str, user_update: UsersUpdate, session: SessionDep):
    db_user = crud_user.get(db=session, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    update_data.pop("tags", None)

    updated_user = crud_user.update(db=session, db_obj=db_user, obj_in=update_data)

    if user_update.tags is not None:
        session.exec(UserTag.__table__.delete().where(UserTag.user_id == user_id))
        session.commit()

        for tag_name in user_update.tags:
            tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
            if not tag:
                tag = crud_tag.create(db=session, obj_in=Tag(name=tag_name))

            user_tag = UserTag(user_id=user_id, tag_id=tag.id)
            crud_user_tag.create(db=session, obj_in=user_tag)

    complete_activities = crud_activity.get_by_field(session, "event_type", "complete")
    if complete_activities:
        complete_activity = complete_activities[0]
        existing_post = session.exec(
            select(Post)
            .where(Post.activity_id == complete_activity.id)
            .where(Post.from_user_id == user_id)
        ).first()

        if not existing_post:
            post_data = PostCreate(
                from_user_id=user_id,
                to_user_id=None,
                activity_id=complete_activity.id,
                status="completed",
            )
            crud_post.create(db=session, obj_in=post_data)

            # Sumar los puntos de la actividad al usuario
            updated_user.total_points += complete_activity.points
            crud_user.update(
                session, updated_user, {"total_points": updated_user.total_points}
            )
            session.commit()

            return updated_user

    return updated_user


@router.delete("/{user_id}", response_model=UsersPublic)
def delete_user(user_id: str, session: SessionDep):
    db_user = crud_user.delete(db=session, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

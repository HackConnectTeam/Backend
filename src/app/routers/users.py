from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from src.app.crud.user import user as crud_user
from src.app.crud.tag import tag as crud_tag
from src.app.crud.user_tag import user_tag as crud_user_tag
from src.app.database import SessionDep
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

    return updated_user


@router.delete("/{user_id}", response_model=UsersPublic)
def delete_user(user_id: str, session: SessionDep):
    db_user = crud_user.delete(db=session, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

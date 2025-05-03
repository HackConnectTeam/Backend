from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from src.app.crud.project import project as crud_project
from src.app.crud.tag import tag as crud_tag
from src.app.crud.project_tag import project_tag as crud_project_tag
from src.app.database import SessionDep
from src.app.models.project import ProjectCreate, ProjectPublic, ProjectUpdate
from src.app.models.project_tag import ProjectTag
from src.app.models.tag import Tag

router = APIRouter(prefix="/project", tags=["project"])


@router.get("/", response_model=List[ProjectPublic])
def read_projects(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_project.get_all(db=session, offset=offset, limit=limit)


@router.get("/{project_id}", response_model=ProjectPublic)
def read_project(project_id: int, session: SessionDep):
    db_project = crud_project.get(db=session, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.post("/", response_model=ProjectPublic)
def create_project(project: ProjectCreate, session: SessionDep):
    project_in = crud_project.create(db=session, obj_in=project)

    for tag_name in project.tags:
        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            tag = crud_tag.create(db=session, obj_in=Tag(name=tag_name))

        project_tag = ProjectTag(project_id=project_in.id, tag_id=tag.id)
        crud_project_tag.create(db=session, obj_in=project_tag)

    return project_in


@router.patch("/{project_id}", response_model=ProjectPublic)
def update_project(project_id: int, project_update: ProjectUpdate, session: SessionDep):
    db_project = crud_project.get(db=session, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud_project.update(db=session, db_obj=db_project, obj_in=project_update)


@router.delete("/{project_id}", response_model=ProjectPublic)
def delete_project(project_id: int, session: SessionDep):
    db_project = crud_project.delete(db=session, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
import requests
from sqlmodel import select
from urllib.parse import urlparse


from src.app.crud.project import project as crud_project
from src.app.crud.tag import tag as crud_tag
from src.app.crud.project_tag import project_tag as crud_project_tag
from src.app.crud.post import post as crud_post
from src.app.crud.user import user as crud_user
from src.app.crud.activity import activity as crud_activity
from src.app.database import SessionDep
from src.app.models.post import Post, PostCreate
from src.app.models.project import Project, ProjectCreate, ProjectPublic, ProjectUpdate
from src.app.models.project_tag import ProjectTag
from src.app.models.tag import Tag

router = APIRouter(prefix="/project", tags=["project"])


def extract_repo_parts(full_url: str) -> tuple[str, str]:
    parsed = urlparse(full_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]
    else:
        raise ValueError("URL de repositorio no válida")


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
def create_project(project: ProjectCreate, session: SessionDep, user_id: str):
    user = crud_user.get(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project_data = Project(**project.model_dump(), user_id=user.id)

    if project.github_repo:
        if "/" not in project.github_repo:
            raise HTTPException(
                status_code=400, detail="Invalid GitHub repo format. Use 'owner/repo'."
            )

    project_in = crud_project.create(db=session, obj_in=project_data)

    for tag_name in project.tags:
        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            tag = crud_tag.create(db=session, obj_in=Tag(name=tag_name))

        project_tag = ProjectTag(project_id=project_in.id, tag_id=tag.id)
        crud_project_tag.create(db=session, obj_in=project_tag)

    if project.github_repo:
        try:
            owner, repo = extract_repo_parts(project.github_repo)
            url = f"https://api.github.com/repos/{owner}/{repo}/languages"
            headers = {"Accept": "application/vnd.github.v3+json"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                langs = response.json().keys()
                for lang in langs:
                    lang_lower = lang.title()
                    tag = session.exec(
                        select(Tag).where(Tag.name == lang_lower)
                    ).first()
                    if not tag:
                        tag = crud_tag.create(db=session, obj_in=Tag(name=lang_lower))
                    exists = session.exec(
                        select(ProjectTag).where(
                            ProjectTag.project_id == project_in.id,
                            ProjectTag.tag_id == tag.id,
                        )
                    ).first()
                    if not exists:
                        project_tag = ProjectTag(
                            project_id=project_in.id, tag_id=tag.id
                        )
                        crud_project_tag.create(db=session, obj_in=project_tag)
            else:
                print(f"GitHub API error: {response.status_code}")
        except Exception as e:
            print(f"Error fetching GitHub languages: {e}")

    create_activities = crud_activity.get_by_field(
        session, "event_type", "complete_project"
    )
    if create_activities:
        create_activity = create_activities[0]

        # Verificar si ya existe un post registrado para esta actividad
        existing_post = session.exec(
            select(Post)
            .where(Post.activity_id == create_activity.id)
            .where(Post.from_user_id == user.id)
        ).first()

        if not existing_post:
            # Crear post para la actividad
            post_data = PostCreate(
                from_user_id=user.id,
                to_user_id=None,
                activity_id=create_activity.id,
                status="completed",
            )
            crud_post.create(db=session, obj_in=post_data)

            # Sumar puntos al usuario
            user.total_points += create_activity.points
            crud_user.update(session, user, {"total_points": user.total_points})
            session.commit()

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

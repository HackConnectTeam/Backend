from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import insert, select

from src.app.database import SessionDep
from src.app.models.project import Project
from src.app.models.team import (
    Team,
    TeamAddMemberResponse,
    TeamAssignProjectResponse,
    TeamCreate,
    TeamJoinResponse,
    TeamPublic,
)
from src.app.crud.team import team as crud_team
from src.app.crud.user import user as crud_user
from src.app.models.team_member import TeamMember


router = APIRouter(prefix="/team", tags=["team"])


@router.get("/teams/", response_model=List[TeamPublic])
def get_teams(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_team.get_all(db=session, offset=offset, limit=limit)


@router.get("/{team_id}", response_model=TeamPublic)
def get_team(team_id: int, session: SessionDep):
    db_team = crud_team.get(db=session, id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.post("/teams/{team_id}/members/{user_id}", response_model=TeamAddMemberResponse)
def add_member_to_team(team_id: int, user_id: str, session: SessionDep):
    session.exec(
        insert(TeamMember)
        .values(team_id=team_id, user_id=user_id)
        .on_conflict_do_nothing()
    )
    session.commit()
    return TeamAddMemberResponse(
        team_id=team_id,
        user_id=user_id,
        message="User added to team",
    )


@router.post("/teams/", response_model=TeamPublic)
def create_team(team: TeamCreate, session: SessionDep):
    db_team = crud_team.create(session, obj_in=team)
    return db_team


@router.post("/teams/{team_id}/join", response_model=TeamJoinResponse)
def join_team(team_id: int, user_id: str, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    user = crud_user.get(session, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = session.exec(
        select(TeamMember).where(
            TeamMember.team_id == team_id, TeamMember.user_id == user_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already in team")

    member = TeamMember(team_id=team_id, user_id=user_id)
    session.add(member)
    session.commit()
    return TeamJoinResponse(
        team_id=team_id,
        user_id=user_id,
        message=f"User {user_id} successfully joined team {team_id}",
    )


@router.post(
    "/teams/{team_id}/assign_project/{project_id}",
    response_model=TeamAssignProjectResponse,
)
def assign_project_to_team(
    team_id: int, project_id: int, user_id: str, session: SessionDep
):
    team = session.get(Team, team_id)
    project = session.get(Project, project_id)

    if not team or not project:
        raise HTTPException(status_code=404, detail="Team or Project not found")

    if project.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="You can only assign your own project"
        )

    project.team_id = team_id
    session.add(project)
    session.commit()
    session.refresh(project)

    return TeamAssignProjectResponse(
        team_id=team_id,
        project_id=project_id,
        project_title=project.title,
        message=f"Project '{project.title}' assigned to team '{team.name}'",
    )

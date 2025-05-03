from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class TeamBase(SQLModel):
    name: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int
    created_at: datetime


class TeamJoinResponse(SQLModel):
    team_id: int
    user_id: str
    status: str = "joined"
    message: str


class TeamAssignProjectResponse(SQLModel):
    team_id: int
    project_id: int
    project_title: str
    status: str = "assigned"
    message: str


class TeamAddMemberResponse(SQLModel):
    team_id: int
    user_id: str
    status: str = "added"
    message: str

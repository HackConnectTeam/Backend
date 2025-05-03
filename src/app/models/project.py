from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel


class ProjectBase(SQLModel):
    title: str
    description_raw: str


class Project(ProjectBase, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    description_ai: Optional[str] = None
    generated_name: Optional[str] = None


class ProjectCreate(ProjectBase):
    tags: List[str]
    team_id: Optional[int] = None


class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    description_raw: Optional[str] = None
    description_ai: Optional[str] = None
    generated_name: Optional[str] = None


class ProjectPublic(ProjectBase):
    id: int
    user_id: str
    created_at: datetime

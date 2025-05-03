from typing import Optional
from sqlmodel import SQLModel, Field


class ProjectTag(SQLModel, table=True):  # type: ignore
    project_id: Optional[int] = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

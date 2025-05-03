from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ActivityBase(SQLModel):
    description: str
    event_type: str
    points: int
    active: bool = True


class Activity(ActivityBase, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    tag_id: int = Field(foreign_key="tag.id")


class ActivityCreate(ActivityBase):
    tag: str


class ActivityUpdate(SQLModel):
    description: Optional[str]
    event_type: Optional[str]
    points: Optional[int]
    active: Optional[bool]


class ActivityPublic(ActivityBase):
    id: int
    created_at: datetime

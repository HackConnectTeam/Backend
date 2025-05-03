from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ChallengeMatchBase(SQLModel):
    from_user_id: int = Field(foreign_key="users.id")
    to_user_id: int = Field(foreign_key="users.id")
    activity_id: int = Field(foreign_key="activity.id")
    status: str = Field(default="pendiente")


class ChallengeMatch(ChallengeMatchBase, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class ChallengeMatchCreate(ChallengeMatchBase):
    pass


class ChallengeMatchUpdate(SQLModel):
    status: Optional[str]
    updated_at: Optional[datetime]


class ChallengeMatchPublic(ChallengeMatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

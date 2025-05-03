from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel


class UsersBase(SQLModel):
    name: str = Field(index=True)


class Users(UsersBase, table=True):  # type: ignore
    id: int = Field(primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    last_active_at: Optional[datetime] = Field(default_factory=datetime.now)
    total_points: int = 0
    nationality: Optional[str] = None


class UsersCreate(UsersBase):
    id: int


class UsersUpdate(SQLModel):
    name: Optional[str]
    last_active_at: Optional[datetime]
    total_points: Optional[int]
    tags: Optional[List[str]] = None
    nationality: Optional[str]


class UsersPublic(UsersBase):
    id: int
    created_at: datetime
    last_active_at: datetime
    total_points: int

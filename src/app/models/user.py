from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel


class UsersBase(SQLModel):
    pass


class Users(UsersBase, table=True):  # type: ignore
    id: str = Field(primary_key=True)
    role: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    last_active_at: Optional[datetime] = Field(default_factory=datetime.now)
    total_points: int = 0
    nationality: Optional[str] = None
    name: Optional[str] = None


class UsersCreate(UsersBase):
    id: str
    role: Optional[str] = Field(default="participant")


class UsersUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None
    last_active_at: Optional[datetime] = None
    total_points: Optional[int] = None
    tags: Optional[List[str]] = None
    nationality: Optional[str] = None


class UsersPublic(UsersBase):
    id: str
    role: str
    created_at: datetime
    last_active_at: datetime
    total_points: int
    name: Optional[str] = None
    nationality: Optional[str] = None

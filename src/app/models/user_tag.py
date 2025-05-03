from typing import Optional
from sqlmodel import SQLModel, Field


class UserTag(SQLModel, table=True):  # type: ignore
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

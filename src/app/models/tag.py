from typing import Optional

from sqlmodel import Field, SQLModel


class TagBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Tag(TagBase, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagPublic(TagBase):
    id: int

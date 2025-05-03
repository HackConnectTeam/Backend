# from datetime import datetime
# from typing import Optional

# from sqlmodel import Field, SQLModel


# class CommentBase(SQLModel):
#     text: str = Field()


# class Comment(CommentBase, table=True):  # type: ignore
#     id: Optional[int] = Field(default=None, primary_key=True)
#     votes: int = Field(default=0)
#     created_at: datetime = Field(default_factory=datetime.now)
#     from_user_id: int = Field(foreign_key="user.id")
#     to_user_id: int = Field(foreign_key="user.id")


# class CommentCreate(CommentBase):
#     text: str
#     from_user_id: int
#     to_user_id: int


# class CommentUpdate(CommentBase):
#     text: Optional[str] = None
#     votes: Optional[int] = None


# class CommentPublic(CommentBase):
#     id: int
#     votes: int
#     created_at: datetime
#     from_user_id: int
#     to_user_id: int

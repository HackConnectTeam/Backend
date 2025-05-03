from typing import Optional
from sqlmodel import SQLModel

from src.app.models.post import PostPublic


class ChallengeResponse(SQLModel):
    status: str
    post: Optional[PostPublic] = None

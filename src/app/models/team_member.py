from sqlmodel import Field, SQLModel


class TeamMember(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    user_id: str = Field(foreign_key="users.id", primary_key=True)

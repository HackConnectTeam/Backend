from sqlmodel import SQLModel


class ImageResponse(SQLModel):
    user_id: str
    img: str

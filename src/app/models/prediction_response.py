from sqlmodel import SQLModel


class PredictionResponse(SQLModel):
    status: str
    message: str

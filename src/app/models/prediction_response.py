from sqlmodel import SQLModel, Field


class PredictionResponse(SQLModel):
    status: str
    message: str

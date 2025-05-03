from pydantic import BaseModel


class NameGenerationRequest(BaseModel):
    project_description: str


class NameGenerationResponse(BaseModel):
    name1: str
    name2: str
    name3: str

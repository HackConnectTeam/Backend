from fastapi import APIRouter

from src.app.schemas.namegeneration import NameGenerationRequest, NameGenerationResponse
from src.app.services.generate_name import generate_names


router = APIRouter()


@router.post("/generate_project_names/", response_model=NameGenerationResponse)
async def generate_project_names(
    request: NameGenerationRequest,
):
    """
    Endpoint to generate project names based on a provided description.
    """
    names_dict = generate_names(request.project_description)
    print(names_dict)
    return NameGenerationResponse(**names_dict)

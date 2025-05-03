from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.app.database import SessionDep
from src.app.models.post import Post, PostCreate
from src.app.schemas.namegeneration import NameGenerationRequest, NameGenerationResponse
from src.app.services.generate_name import generate_names
from src.app.crud.user import user as crud_user
from src.app.crud.post import post as crud_post
from src.app.crud.activity import activity as crud_activity


router = APIRouter()


@router.post("/generate_project_names/", response_model=NameGenerationResponse)
async def generate_project_names(
    request: NameGenerationRequest, session: SessionDep, user_id: str
):
    """
    Endpoint to generate project names based on a provided description.
    """

    user = crud_user.get(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    names_dict = generate_names(request.project_description)

    generate_activities = crud_activity.get_by_field(
        session, "event_type", "generate_names"
    )
    if generate_activities:
        generate_activity = generate_activities[0]

        # Verificar si ya se registró esta actividad para el usuario
        existing_post = session.exec(
            select(Post)
            .where(Post.activity_id == generate_activity.id)
            .where(Post.from_user_id == user.id)
        ).first()

        if not existing_post:
            # Crear el post
            post_data = PostCreate(
                from_user_id=user.id,
                to_user_id=None,
                activity_id=generate_activity.id,
                status="completed",
            )
            crud_post.create(db=session, obj_in=post_data)

            # Sumar los puntos al usuario
            user.total_points += generate_activity.points
            crud_user.update(session, user, {"total_points": user.total_points})
            session.commit()

    return NameGenerationResponse(**names_dict)

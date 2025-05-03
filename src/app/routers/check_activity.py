from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from src.app.crud.user import user as crud_user
from src.app.crud.activity import activity as crud_activity
from src.app.crud.tag import tag as crud_tag
from src.app.crud.post import post as crud_post
from src.app.database import SessionDep
from src.app.models.post import Post, PostCreate
from src.app.models.user_tag import UserTag
from src.app.schemas.challenge import ChallengeResponse

router = APIRouter()


@router.get("/check_challenge/{activity_id}", response_model=ChallengeResponse)
def check_challenge(
    activity_id: int,
    session: SessionDep,
    completing_user_id: str = Query(...),
    tagged_user_id: str = Query(...),
):
    """
    Checks if a user has completed a challenge associated with an activity.
    """
    # 1. Look up the completing user.
    completing_user = crud_user.get(session, completing_user_id)
    if not completing_user:
        raise HTTPException(status_code=404, detail="Completing user not found")

    # 2. Look up the activity.
    activity = crud_activity.get(session, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # 3. Get the tag associated with the activity.
    activity_tag = crud_tag.get(session, activity.tag_id)
    if not activity_tag:
        raise HTTPException(
            status_code=404, detail="Tag associated with activity not found"
        )

    # 4.  Check if the user has the tag.
    user_tag = session.exec(
        select(UserTag)
        .where(UserTag.user_id == tagged_user_id)
        .where(UserTag.tag_id == activity_tag.id)
    ).first()

    status = "completed" if user_tag else "failed"
    new_post = None

    existing_post = session.exec(
        select(Post).where(
            Post.from_user_id == completing_user_id, Post.activity_id == activity_id
        )
    ).first()
    if existing_post:
        return ChallengeResponse(status="failed", post=None)

    if status == "completed":
        # 6. Create the post
        post_data = PostCreate(
            from_user_id=completing_user_id,
            to_user_id=tagged_user_id,
            activity_id=activity_id,
            status=status,
        )
        new_post = crud_post.create(db=session, obj_in=post_data)

        # 7. Update user points
        completing_user.total_points += activity.points
        crud_user.update(
            session, completing_user, {"total_points": completing_user.total_points}
        )

    return ChallengeResponse(status=status, post=new_post)

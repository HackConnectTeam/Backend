import base64

from fastapi import APIRouter, Body, HTTPException
from loguru import logger

from src.app.config.config import settings
from src.app.models.ImageResponse import ImageResponse
from src.app.utils.minio_utils import retrieve_file, get_s3

router = APIRouter(prefix="/img_retrieval", tags=["Avatar Image Retrieval"])


@router.post(
    "/",
    response_model=ImageResponse,
    summary="Generate a Mii from a user at the photo",
)
async def predict(
    user_id: str = Body(..., description="Unique user id"),
):
    try:
        print(f"{user_id}")
        logger.info(f"{user_id}")
        logger.info(f"{settings.s3.bucket_name}")
        dict_image = retrieve_file(
            s3=get_s3(),
            img_path=settings.s3.bucket_name
            + "/"
            + settings.s3.folder
            + "/"
            + settings.s3.result_folder
            + "/"
            + user_id,
        )

        image = next(iter(dict_image.values()))

        img_b64 = base64.b64encode(image).decode("utf-8")

        return {"user_id": user_id, "img": img_b64}
    except Exception:
        raise HTTPException(status_code=500, detail="Mii Creation Failed")

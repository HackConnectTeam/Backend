import base64
import io

from PIL import Image
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
        logger.info(f"{dict_image}")
        # Convert the image to base64
        im = Image.fromarray(dict_image[user_id].astype("uint8"))
        logger.info(f"{im}")
        rawBytes = io.BytesIO()
        im.save(rawBytes, "PNG")
        rawBytes.seek(0)
        img_b64 = base64.b64encode(rawBytes.read())

        return {"user_id": user_id, "img": img_b64}
    except Exception:
        raise HTTPException(status_code=500, detail="Mii Creation Failed")

import base64
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException
from src.app.schemas.base import Base64ImageRequest
from src.app.utils.api_utils import inference_task

from src.app.models.prediction_response import PredictionResponse

router = APIRouter(prefix="/to_mii", tags=["Avatar Inference"])


@router.post(
    "/",
    response_model=PredictionResponse,
    summary="Perform inference with user id and image path",
)
async def predict(
    background_tasks: BackgroundTasks,
    request: Base64ImageRequest,
    user_id: str = Body(..., description="Unique user id"),
):
    try:
        image_data = base64.b64decode(request.image_base64)

        # Call the inference function asynchronously
        background_tasks.add_task(inference_task, user_id, image_data)

        return {
            "status": "success",
            "message": f"Prediction for user: {user_id} added to the queue.",
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Mii Creation Failed")

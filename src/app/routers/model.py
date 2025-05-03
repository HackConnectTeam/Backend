from fastapi import APIRouter, BackgroundTasks, Body
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
    user_id: str = Body(..., description="Unique user id"),
    image_path: str = Body(
        ..., description="Path (from the bucket) to the image for inference"
    ),
):
    # Call the inference function asynchronously
    background_tasks.add_task(inference_task, [user_id], [image_path])

    return {
        "status": "success",
        "message": f"Prediction for user: {user_id} added to the queue.",
    }

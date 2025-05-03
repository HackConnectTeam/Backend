import io
import json
from http.client import HTTPException

import requests
from PIL import Image
from loguru import logger

from src.app.config.config import settings
from src.app.utils.minio_utils import get_s3, upload_images


def build_inference_url(
    model_settings_path: str = "config/model_config/model-settings.json",
    settings_path: str = "config/settings.json",
) -> str:
    """
    Build the URL for the inference endpoint.
    :param model_settings_path: Path to the model settings file.
    :param settings_path: Path to the settings file.
    """

    # Read the model settings and settings files
    model_settings = json.load(open(model_settings_path))
    settings = json.load(open(settings_path))

    # Extract the model name, host and port
    model_name = model_settings["name"]
    host = settings["host"]
    port = settings["http_port"]

    return f"http://{host}:{port}/v2/models/{model_name}/infer"


def inference_task(user_id: str, image_data: bytes):
    """
    Perform inference on the provided images and parcel ID.
    :param user: ID of the user
    :param image: Image
    :return:
    """
    # Build the inference URL where the model is dettingeployed
    inference_url = build_inference_url()

    if not user_id or not image_data:
        raise HTTPException()

    # To PIL image
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # Build the minio path
    image_path = settings.s3.bucket_name + "/" + settings.s3.folder + "/" + user_id[0]

    # Upload the image to MinIO
    upload_images(
        s3=get_s3(),
        minio_path=image_path[0],
        images={user_id[0]: image},
    )

    data = {
        "inputs": [
            {
                "name": "user_id",
                "shape": [1],
                "datatype": "BYTES",
                "data": user_id,
            },
            {
                "name": "image_path",
                "shape": [1],
                "datatype": "BYTES",
                "data": image_path,
            },
        ]
    }

    logger.info(f"Inference request: {data}")
    logger.info(f"Inference URL: {inference_url}")
    response = requests.post(inference_url, json=data)

    if response.status_code != 200:
        logger.error(f"Error in inference: {response.text}")
        raise HTTPException()

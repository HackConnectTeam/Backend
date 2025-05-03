import json
from http.client import HTTPException

import requests
from loguru import logger


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

    return f"https://{host}/v2/models/{model_name}/infer"


def inference_task(user_id: str, image_path: str):
    """
    Perform inference on the provided images and parcel ID.
    :param user: ID of the user
    :param image_path: Path of the folder with image
    :return:
    """
    # Build the inference URL where the model is dettingeployed
    inference_url = build_inference_url()

    if not user_id or not image_path:
        raise HTTPException()

    data = {
        "inputs": [
            {"name": "user_id", "shape": [1], "datatype": "BYTES", "data": [user_id]},
            {
                "name": "image_path",
                "shape": [1],
                "datatype": "BYTES",
                "data": [image_path],
            },
        ]
    }

    logger.info(f"Inference request: {data}")
    logger.info(f"Inference URL: {inference_url}")
    response = requests.post(inference_url, json=data)

    if response.status_code != 200:
        raise HTTPException()

    response = response.json()
    print(response)

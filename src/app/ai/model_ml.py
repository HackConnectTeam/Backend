import json
from typing import List, Optional

import torch
from loguru import logger
from mlserver import MLModel
from mlserver.codecs import decode_args
from PIL import Image
from transformers import pipeline
from diffusers import (
    StableDiffusionControlNetImg2ImgPipeline,
    ControlNetModel,
    UniPCMultistepScheduler,
)
from src.app.config.config import settings
from src.app.utils.image_utils import get_depth_map
from src.app.utils.minio_utils import get_s3, upload_images, retrieve_file


class Model(MLModel):
    async def process_images(self, image: dict[str, Image]) -> torch.Tensor:
        """
        Preprocess the image to be used by the model.
        :param image: Image in cache to process
        :return: Preprocessed image and depth map
        """

        # Get the image from the dictionary
        image = next(iter(image.values()))
        print(f"sizeeeee {image.size}")
        # Resize to lower resolution
        image = image.resize(
            (image.size[0] // 3, image.size[1] // 3), resample=Image.Resampling.LANCZOS
        )

        # Compute the depth map
        depth_map = get_depth_map(image, self._estimator).unsqueeze(0).half().to("cuda")

        # Free cuda cache
        torch.cuda.empty_cache()

        return image, depth_map

    async def load(self) -> bool:
        """
        Load the model and S3 client.
        :return: True if the model was loaded successfully
        """

        logger.info("Loading Control Net...")

        # ControlNet model
        self._controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11f1p_sd15_depth",
            torch_dtype=torch.float16,
            use_safetensors=True,
            cache_dir="./model_cache",
        )

        logger.info("Loading Stable Difussion...")

        # Pipeline for Stable Diffusion with ControlNet
        self._predictive = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=self._controlnet,
            torch_dtype=torch.float16,
            use_safetensors=True,
            cache_dir="./model_cache",
        )

        # Apply memory optimizations
        self._predictive.scheduler = UniPCMultistepScheduler.from_config(
            self._predictive.scheduler.config
        )
        self._predictive.enable_model_cpu_offload()
        self._predictive.enable_vae_slicing()
        self._predictive.enable_attention_slicing()

        # Estimator for depth estimation
        self._estimator = pipeline("depth-estimation", device="cpu")

        # Get the S3 client
        self._s3_client = get_s3()

        logger.info("All models have been loaded!!!")

        return True

    @decode_args
    async def predict(
        self,
        user_id: Optional[List[str]] = None,
        image_path: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Perform inference on the image using the model.
        :param user_id: ID of the user
        :param image_path: Path of the image

        :return: Prediction of the model
        """

        # Search for the files in the S3 bucket
        dict_images = retrieve_file(s3=self._s3_client, img_path=image_path[0])

        # Preprocess the images
        logger.info("Processing images")
        image, depth_map = await self.process_images(dict_images)

        logger.info("Prediction images")
        # Make the prediction with the model deployed
        output = self._predictive(
            prompt="Image of person to Mii avatar from Wii",
            image=image,
            control_image=depth_map,
            num_inference_steps=20,
            guidance_scale=7.5,
        ).images[0]

        logger.info("Uploading image")
        # Upload the results to the S3 bucket
        upload_images(
            s3=self._s3_client,
            minio_path=settings.s3.bucket_name
            + "/"
            + settings.s3.folder
            + "/"
            + settings.s3.result_folder
            + "/"
            + user_id[0],
            images={user_id[0]: output},
        )

        return [json.dumps({"message": "Success"})]

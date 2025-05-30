import io
from pathlib import Path

import numpy as np
import s3fs
from PIL import Image
from loguru import logger

from src.app.config.config import settings


def get_s3(
    endpoint_url: str = settings.s3.storage_url,
    access_key: str = settings.minio.access_key,
    secret_key: str = settings.minio.secret_key,
):
    """
    Get an S3 filesystem object.
    :param endpoint_url: URL of the S3 storage
    :param access_key: Access key for the S3 bucket
    :param secret_key: Secret key for the S3 bucket

    :return: S3 filesystem object
    """
    return s3fs.S3FileSystem(
        endpoint_url=endpoint_url, key=access_key, secret=secret_key
    )


def retrieve_file(
    s3: s3fs.S3FileSystem,
    img_path: str,
    bucket_name: str = settings.s3.bucket_name,
    folder: str = settings.s3.folder,
) -> dict:
    """
    List all files in an S3 bucket.
    :param s3: S3 filesystem object
    :param files: list of files to search
    :param bucket_name: Name of the bucket
    :return: Dictionary of file names and their contents
    """

    dict = {}

    if s3.ls(bucket_name):
        if (
            img_path.split("/")[-1].endswith(".jpg")
            or img_path.split("/")[-1].endswith(".png")
            or img_path.split("/")[-1].endswith(".jpeg")
        ):
            with s3.open(img_path, "rb") as file:
                img = Image.open(io.BytesIO(file.read()))
                dict[img_path] = np.array(img)
    else:
        logger.error(
            f'Folder {folder} does not exist in bucket {bucket_name + f"/{folder}/"}'
        )

    return dict


def upload_image(
    s3: s3fs.S3FileSystem, minio_path: str, img_info: tuple[str, Image]
) -> bool:
    """
    Upload an image to an S3 bucket.
    :param s3: S3 filesystem object
    :param minio_path: Path in the bucket to upload the image
    :param img: Image to upload

    :return: True if the upload was successful, False otherwise
    """

    img_name, image = img_info
    try:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        content_length = buffer.tell()
        buffer.seek(0)
        # Upload to MinIO
        img_name = img_name.replace(".jpg", ".png")
        img_name = img_name.split("/")[-1]
        logger.info(f"Uploading to {minio_path}")
        with s3.open(
            minio_path,
            "wb",
            headers={"Content-Length": str(content_length)},
        ) as file:
            file.write(buffer.getvalue())
        return True
    except Exception as e:
        logger.error(f"Failed to upload {img_name} to {minio_path}: {e}")
    return False


def upload_images(
    s3: s3fs.S3FileSystem, minio_path: str | Path, images: dict[str, Image]
) -> bool:
    """
    Upload multiple images to an S3 bucket.

    :param s3: S3 filesystem object
    :param minio_path: Path in the bucket to upload the images
    :param img_paths: List of image file paths to upload
    :return: List of successfully uploaded image paths in S3
    """

    for img_name, img in images.items():
        logger.info(f"Uploading {img_name} to {minio_path}")
        img_name = img_name.split("/")[-1]
        if not upload_image(s3, minio_path, (img_name, img)):
            logger.error(f"Failed to upload {img_name} to {minio_path}")
            return False

    return True


if __name__ == "__main__":
    s3 = get_s3()
    upload_image(
        s3, "images", ("jandro.jpeg", Image.open("/opt/project/data/jandro.jpeg"))
    )

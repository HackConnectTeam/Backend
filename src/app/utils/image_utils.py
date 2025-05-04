import numpy as np
import torch
from PIL import Image


def get_depth_map(image, depth_estimator):
    depth = depth_estimator(image)["depth"]
    depth = np.array(depth)
    depth = depth[:, :, None]
    depth = np.concatenate([depth] * 3, axis=2)
    depth_tensor = torch.from_numpy(depth).float() / 255.0
    return depth_tensor.permute(2, 0, 1)


def resize_image(image: Image) -> Image:
    """
    Resizes the image so that its maximum dimension does not exceed 512,
    maintaining the aspect ratio.

    :param image: A PIL.Image object
    :return: Resized image
    """
    # Get the original dimensions of the image
    width, height = image.size

    # If both dimensions are already smaller than or equal to 512, do nothing
    if width <= 512 and height <= 512:
        return image

    # Calculate the scaling factor to maintain the aspect ratio
    if width > height:
        scale_factor = 512 / width
    else:
        scale_factor = 512 / height

    # Calculate the new dimensions
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Resize the image while maintaining the aspect ratio
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return resized_image

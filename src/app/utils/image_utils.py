import numpy as np
import torch

def get_depth_map(image, depth_estimator):
    depth = depth_estimator(image)["depth"]
    depth = np.array(depth)
    depth = depth[:, :, None]
    depth = np.concatenate([depth] * 3, axis=2)
    depth_tensor = torch.from_numpy(depth).float() / 255.0
    return depth_tensor.permute(2, 0, 1)
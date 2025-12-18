import torch
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def estimate_depth(image_path, output_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load two MiDaS models for hybrid estimation
    midas_large = torch.hub.load("intel-isl/MiDaS", "DPT_Large").to(device).eval()
    midas_hybrid = torch.hub.load("intel-isl/MiDaS", "DPT_Hybrid").to(device).eval()

    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform_large = transforms.dpt_transform
    transform_hybrid = transforms.dpt_transform

    # Load image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Transform images for both models
    input_large = transform_large(img_rgb).to(device)
    input_hybrid = transform_hybrid(img_rgb).to(device)

    with torch.no_grad():
        depth_large = midas_large(input_large)
        depth_large = torch.nn.functional.interpolate(
            depth_large.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()

        depth_hybrid = midas_hybrid(input_hybrid)
        depth_hybrid = torch.nn.functional.interpolate(
            depth_hybrid.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()

    # Convert to numpy
    depth_large = depth_large.cpu().numpy()
    depth_hybrid = depth_hybrid.cpu().numpy()

    # Hybrid depth: average
    depth_map = (depth_large + depth_hybrid) / 2.0

    # Filtering to smooth noise
    depth_map = cv2.bilateralFilter(depth_map.astype(np.float32), d=5, sigmaColor=0.05, sigmaSpace=5)

    # Normalize depth map
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.imsave(output_path, depth_map, cmap="inferno")

    print(f"[OK] Hybrid & filtered depth map saved to: {output_path}")
    return depth_map

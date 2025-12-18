import cv2
import numpy as np

def build_scene(image_path, depth_map):
    image = cv2.imread(image_path)
    h, w = depth_map.shape

    scene = []
    for y in range(0, h, 5):
        for x in range(0, w, 5):
            z = depth_map[y, x]
            color = image[y, x]
            scene.append((x, y, z, color))

    return scene

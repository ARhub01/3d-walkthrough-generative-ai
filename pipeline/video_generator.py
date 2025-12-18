import cv2
import numpy as np
import os

def generate_video(frames, output_path, width, height):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        10,
        (width, height)
    )

    for frame_data in frames:
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        for x, y, color in frame_data:
            if 0 <= x < width and 0 <= y < height:
                frame[y, x] = color

        # Optional: apply slight Gaussian blur for smoothness
        frame = cv2.GaussianBlur(frame, (3, 3), 0)

        video.write(frame)

    video.release()

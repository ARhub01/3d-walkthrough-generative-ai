# generate_walkthrough.py
import os
import cv2
import numpy as np
from pipeline.depth_estimation import estimate_depth
from pipeline.scene_builder import build_scene
from llm.scene_planner import generate_camera_plan
from pipeline.camera_controller import generate_camera_frames
from pipeline.video_generator import generate_video
import math

# -----------------------------
# Configuration
# -----------------------------
INPUT_FOLDER = "data/input/"
DEPTH_FOLDER = "outputs/depth/"
VIDEO_FOLDER = "outputs/video/"
PIXEL_SKIP = 4  # for performance (sparse point sampling)
PREVIEW = True  # show depth map and sample frames

# -----------------------------
# Helper: Layered camera shift with easing
# -----------------------------
def apply_easing(t):
    """Ease-in-out cubic"""
    return 3*t**2 - 2*t**3

# -----------------------------
# Process each image
# -----------------------------
for img_file in os.listdir(INPUT_FOLDER):
    if not img_file.endswith((".jpg", ".png")):
        continue

    img_path = os.path.join(INPUT_FOLDER, img_file)
    depth_path = os.path.join(DEPTH_FOLDER, f"{img_file}_depth.png")
    video_path = os.path.join(VIDEO_FOLDER, f"{img_file}_walkthrough.mp4")

    print(f"[INFO] Processing {img_file} ...")

    # 1️⃣ Depth estimation
    depth_map = estimate_depth(img_path, depth_path)

    # Optional preview of depth
    if PREVIEW:
        depth_preview = (depth_map * 255).astype(np.uint8)
        cv2.imshow("Depth Map", depth_preview)
        cv2.waitKey(500)

    # 2️⃣ Build 3D scene (sparse)
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    scene = []
    for y in range(0, h, PIXEL_SKIP):
        for x in range(0, w, PIXEL_SKIP):
            z = depth_map[y, x]
            color = img[y, x]
            scene.append((x, y, z, color))

    # 3️⃣ Generate camera plan
    prompt = "Create a smooth cinematic walkthrough of a living room"
    camera_plan = generate_camera_plan(prompt)

    # 4️⃣ Generate multi-layer frames with easing & parallax
    frames = []
    for i, step in enumerate(camera_plan["path"]):
        t = i / max(len(camera_plan["path"])-1, 1)
        ease = apply_easing(t)

        foreground = [p for p in scene if p[2] < 0.3]
        midground = [p for p in scene if 0.3 <= p[2] < 0.7]
        background = [p for p in scene if p[2] >= 0.7]

        frame = []

        def shift_points(points, factor):
            shifted = []
            for x, y, z, color in points:
                # Apply easing + slight rotation
                shifted_x = int(x + step["x"] * factor * ease)
                shifted_y = int(y + step["z"] * factor * ease + 5*math.sin(t*2*math.pi))
                shifted.append((shifted_x, shifted_y, color))
            return shifted

        frame += shift_points(foreground, factor=60)
        frame += shift_points(midground, factor=40)
        frame += shift_points(background, factor=20)
        frames.append(frame)

    # Optional preview first few frames
    if PREVIEW:
        for fidx, frame_data in enumerate(frames[:10]):
            frame_img = np.zeros((h, w, 3), dtype=np.uint8)
            for x, y, color in frame_data:
                for dx in range(2):
                    for dy in range(2):
                        if 0 <= x+dx < w and 0 <= y+dy < h:
                            frame_img[y+dy, x+dx] = color
            cv2.imshow("Frame Preview", frame_img)
            cv2.waitKey(100)
        cv2.destroyAllWindows()

    # 5️⃣ Generate video (with optional small Gaussian blur)
    generate_video(frames, video_path, w, h)

    print(f"[DONE] Video saved at: {video_path}")

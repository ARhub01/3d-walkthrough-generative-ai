import numpy as np

def generate_camera_frames(scene, camera_plan):
    """
    Generates frames with multi-layer motion for cinematic effect.
    scene: list of (x, y, z, color)
    camera_plan: dict with 'path' (list of steps) and 'speed'
    """
    frames = []

    # Divide scene into layers by depth (z)
    foreground = [p for p in scene if p[2] < 0.3]
    midground = [p for p in scene if 0.3 <= p[2] < 0.7]
    background = [p for p in scene if p[2] >= 0.7]

    for step in camera_plan["path"]:
        frame = []

        def shift_points(points, factor):
            shifted = []
            for x, y, z, color in points:
                shifted_x = int(x + step["x"] * factor)
                shifted_y = int(y + step["z"] * factor)
                shifted.append((shifted_x, shifted_y, color))
            return shifted

        # Apply different shift factors per layer
        frame += shift_points(foreground, factor=60)   # foreground moves more
        frame += shift_points(midground, factor=40)    # midground
        frame += shift_points(background, factor=20)   # background moves less

        frames.append(frame)

    return frames

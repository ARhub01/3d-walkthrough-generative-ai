# 3D Walkthrough Generative AI

A cinematic 3D walkthrough generator that converts a single 2D room image into a smooth video using AI-powered depth estimation and generative camera motion.

---

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

---

## **Overview**
This project leverages **deep learning** and **generative AI** to create 3D walkthroughs from single images:

1. **Hybrid Depth Estimation**: Combines MiDaS DPT_Large and DPT_Hybrid models for robust depth maps.
2. **Scene Construction**: Converts depth maps into layered 3D point clouds.
3. **Cinematic Camera Motion**: Multi-layer parallax with easing, rotation, and zoom effects.
4. **Video Generation**: Outputs smooth walkthrough videos with optional Gaussian smoothing.
5. **Batch Processing**: Automatically generates videos for multiple room images.

This end-to-end pipeline is designed for **AI-powered visualization, interior design previews, and portfolio demonstrations**.

---

## **Features**
- Hybrid depth estimation with noise filtering
- Multi-layer parallax camera motion
- Smooth easing and subtle rotation for cinematic effect
- Sparse point selection for performance optimization
- Interactive previews of depth maps and frames
- Batch processing of multiple room images
- Output: MP4 walkthrough videos

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/yourusername/3d-walkthrough-generative-ai.git
cd 3d-walkthrough-generative-ai
```
Create a virtual environment:
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows


Install required packages:
```
pip install -r requirements.txt
```

(Optional) Set OpenAI API key for LLM-based camera planner:
```
export OPENAI_API_KEY="your_api_key_here"  # Linux / Mac
setx OPENAI_API_KEY "your_api_key_here"    # Windows
```
**Usage**

Place your input images in data/input/:
```
data/input/room1.jpg
data/input/room2.jpg
```

Run the walkthrough pipeline:
```
python generate_walkthrough.py
```

Outputs will be saved in:
```
outputs/depth/      # Depth maps
outputs/video/      # Walkthrough videos
```

Interactive previews will show depth maps and sample frames during processing.

**Project Structure**
3d-walkthrough-generative-ai/
├── data/
│   └── input/                # Input room images
├── outputs/
│   ├── depth/                # Depth map outputs
│   └── video/                # Generated walkthrough videos
├── pipeline/
│   ├── depth_estimation.py   # Hybrid depth estimation
│   ├── scene_builder.py      # Build 3D scene from depth
│   ├── camera_controller.py  # Multi-layer camera frames
│   └── video_generator.py    # Video rendering
├── llm/
│   └── scene_planner.py      # LLM/fallback camera plan
├── generate_walkthrough.py   # Main pipeline script
└── requirements.txt

**Future Improvements**

Replace point cloud rendering with meshes and textures for more realistic visuals.

Support interactive 3D preview in GUI.

Add advanced camera path variations (zoom, tilt, dynamic rotation).

Optimize performance further for ultra-high-resolution images.

Integrate multi-scene compositing and automatic scene stitching.
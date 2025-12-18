import json
import os

def _fallback_camera_plan():
    # Deterministic camera path (no LLM)
    return {
        "path": [
            {"x": 0.0, "y": 0.0, "z": 0.0},
            {"x": 0.0, "y": 0.0, "z": -0.5},
            {"x": 0.3, "y": 0.0, "z": -1.0},
            {"x": 0.6, "y": 0.0, "z": -1.5}
        ],
        "speed": 1.0,
        "mode": "fallback"
    }

def generate_camera_plan(prompt: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")

    # If no API key → use fallback
    if not api_key:
        print("[INFO] No OPENAI_API_KEY found. Using fallback camera planner.")
        return _fallback_camera_plan()

    # If key exists → LLM mode (kept for future use)
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    system_prompt = """
You convert scene descriptions into camera motion paths.
Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return json.loads(response.choices[0].message.content)

from __future__ import annotations

"""Fast regression test for the MoviePy/PIL subtitle rendering path."""

import json
import math
import wave
from pathlib import Path

import numpy as np
from PIL import Image

from studio.engine import render


def make_wav(path: Path, seconds: float = 2.0, rate: int = 22050) -> None:
    frames = bytearray()
    for i in range(int(seconds * rate)):
        sample = int(8000 * math.sin(2 * math.pi * 440 * i / rate))
        frames += int(sample).to_bytes(2, "little", signed=True)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(frames)


def test_renderer_accepts_pil_subtitle_frames(tmp_path: Path) -> None:
    image = tmp_path / "scene.png"
    Image.new("RGB", (640, 360), (30, 30, 30)).save(image)
    audio = tmp_path / "voice.wav"
    make_wav(audio)
    subtitles = tmp_path / "subtitles.json"
    subtitles.write_text(json.dumps([{
        "start_time": 0.0,
        "end_time": 1.5,
        "text": "Bitcoin liquidity without selling",
        "words": [
            {"word": "Bitcoin", "start": 0.0, "end": 0.35},
            {"word": "liquidity", "start": 0.35, "end": 0.75},
            {"word": "without", "start": 0.75, "end": 1.05},
            {"word": "selling", "start": 1.05, "end": 1.5},
        ],
    }]), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "resolution": [640, 360],
        "fps": 24,
        "crf": 28,
        "bitrate": "1200k",
        "audio_bitrate": "96k",
        "preset": "ultrafast",
        "seed": 42,
        "scenes": [{"asset": str(image), "duration": 2.0, "camera": "center", "transition": "fade", "crop": "cover"}],
        "audio": str(audio),
        "enhanced_subtitle": str(subtitles),
        "subtitles": {"font_size": 28, "bottom_margin": 20},
    }), encoding="utf-8")
    output = tmp_path / "smoke.mp4"
    render(manifest, output)
    assert output.exists() and output.stat().st_size > 0

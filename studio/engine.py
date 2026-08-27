"""Reusable cinematic renderer for Pawan Video Studio.

The Studio layer sits above the existing MoneyPrinterTurbo pipeline. Projects
change; the renderer stays. Product screenshots remain authentic source assets,
while motion, captions, timing and composition are generated dynamically.
"""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger
from moviepy import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip, VideoFileClip
from moviepy.video.fx import Resize
from PIL import Image, ImageDraw, ImageFont


@dataclass
class Scene:
    asset: str
    duration: float | None = None
    camera: str = "auto"
    transition: str = "fade"
    crop: str = "cover"
    subtitle_style: str | None = None
    overlay: str | None = None


CAMERA_STYLES = (
    "push_in", "pull_out", "pan_left", "pan_right", "pan_up", "pan_down",
    "drift_left", "drift_right", "drift_up", "drift_down", "center", "auto",
)


def _parse_srt_timestamp(value: str) -> float:
    h, m, rest = value.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def read_srt(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", text.strip())
    result: list[dict[str, Any]] = []
    for block in blocks:
        lines = [x.strip() for x in block.splitlines() if x.strip()]
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start, end = [x.strip() for x in lines[1].split("-->", 1)]
        result.append({"start": _parse_srt_timestamp(start), "end": _parse_srt_timestamp(end), "text": " ".join(lines[2:])})
    return result


def read_enhanced_subtitles(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception as exc:
        logger.warning(f"Could not read enhanced subtitles: {exc}")
        return []


def _font(size: int, font_path: str | None = None):
    candidates = [font_path] if font_path else []
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def _wrap_words(text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)
    for word in words:
        candidate = word if not current else f"{current} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=font, stroke_width=0)
        if bbox[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:2]


def make_caption_image(text: str, width: int, font_size: int = 56,
                       text_color=(255, 255, 255, 255),
                       box_color=(0, 0, 0, 165), font_path: str | None = None) -> Image.Image:
    """Create a compact safe-area caption; never a giant full-screen subtitle."""
    font = _font(font_size, font_path)
    lines = _wrap_words(text, font, int(width * 0.86))
    dummy = Image.new("RGBA", (width, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy)
    spacing = max(8, font_size // 6)
    boxes = [draw.textbbox((0, 0), line, font=font, stroke_width=2) for line in lines]
    text_h = sum(b[3] - b[1] for b in boxes) + spacing * max(0, len(lines) - 1)
    pad_x, pad_y = 28, 18
    box_w = min(width - 48, max(b[2] - b[0] for b in boxes) + pad_x * 2)
    box_h = text_h + pad_y * 2
    img = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, box_w - 1, box_h - 1), radius=24, fill=box_color)
    y = pad_y
    for b, line in zip(boxes, lines):
        tw = b[2] - b[0]
        x = (box_w - tw) // 2
        draw.text((x, y), line, font=font, fill=text_color, stroke_width=2, stroke_fill=(0, 0, 0, 210))
        y += (b[3] - b[1]) + spacing
    return img


def _camera_key(style: str, seed: int) -> str:
    if style != "auto":
        return style
    return random.Random(seed).choice(CAMERA_STYLES[:-1])


def apply_camera_motion(clip, width: int, height: int, style: str, seed: int):
    """Apply restrained cinematic camera movement to images or video."""
    style = _camera_key(style if style in CAMERA_STYLES else "auto", seed)
    moving = {"push_in", "pull_out", "pan_left", "pan_right", "pan_up", "pan_down",
              "drift_left", "drift_right", "drift_up", "drift_down"}
    if style not in moving:
        return clip.with_position("center")

    if style == "pull_out":
        start_scale, end_scale = 1.10, 1.04
    elif style == "push_in":
        start_scale, end_scale = 1.04, 1.10
    else:
        start_scale, end_scale = 1.07, 1.07

    clip = clip.with_effects([Resize(lambda t: start_scale + (end_scale - start_scale) * (t / max(clip.duration, 0.001)))])
    # The clip is already scaled to cover the output frame. These offsets are
    # intentionally small so UI text remains readable.
    travel_x = max(0.0, clip.w - width) * 0.72
    travel_y = max(0.0, clip.h - height) * 0.72

    def pos(t):
        p = min(1.0, max(0.0, t / max(clip.duration, 0.001)))
        if style in {"pan_left", "drift_left"}:
            return (-travel_x * p, (height - clip.h) / 2)
        if style in {"pan_right", "drift_right"}:
            return (-travel_x * (1 - p), (height - clip.h) / 2)
        if style in {"pan_up", "drift_up"}:
            return ((width - clip.w) / 2, -travel_y * p)
        if style in {"pan_down", "drift_down"}:
            return ((width - clip.w) / 2, -travel_y * (1 - p))
        return ((width - clip.w) / 2, (height - clip.h) / 2)

    return clip.with_position(pos)


def _load_media(path: str, duration: float, width: int, height: int):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        clip = ImageClip(str(p)).with_duration(duration)
    else:
        source = VideoFileClip(str(p))
        clip_duration = min(duration, source.duration)
        clip = source.subclipped(0, clip_duration)
        if clip_duration < duration:
            clip = clip.with_duration(duration)

    scale = max(width / clip.w, height / clip.h)
    clip = clip.resized(scale)
    background = ColorClip((width, height), color=(8, 10, 14)).with_duration(duration)
    return CompositeVideoClip([background, clip.with_position("center")], size=(width, height)).with_duration(duration)


def render(manifest: str | Path | dict[str, Any], output: str | Path) -> str:
    """Render a Studio manifest to MP4."""
    spec = json.loads(Path(manifest).read_text(encoding="utf-8")) if isinstance(manifest, (str, Path)) else manifest
    width, height = spec.get("resolution", [1080, 1920])
    seed = int(spec.get("seed", 42))
    scenes = [Scene(**s) for s in spec["scenes"]]
    audio_path = spec.get("audio")
    srt_path = spec.get("subtitle")
    enhanced_path = spec.get("enhanced_subtitle")
    subtitle_cfg = spec.get("subtitles", {})
    font_size = int(subtitle_cfg.get("font_size", 54))
    font_path = subtitle_cfg.get("font_path")
    subtitle_gap = float(subtitle_cfg.get("bottom_margin", 120))

    audio = AudioFileClip(audio_path) if audio_path else None
    total = audio.duration if audio else sum((s.duration or 0) for s in scenes)
    clips = []
    cursor = 0.0
    for idx, scene in enumerate(scenes):
        remaining = max(0.1, total - cursor)
        duration = min(float(scene.duration or spec.get("default_scene_duration", 4.5)), remaining)
        base = _load_media(scene.asset, duration, width, height)
        base = apply_camera_motion(base, width, height, scene.camera, seed + idx * 1009)
        clips.append(base.with_start(cursor))
        cursor += duration
        if cursor >= total - 0.01:
            break

    if not clips:
        raise ValueError("Studio manifest contains no renderable scenes")
    timeline = CompositeVideoClip(clips, size=(width, height)).with_duration(total)

    enhanced = read_enhanced_subtitles(enhanced_path) if enhanced_path else []
    srt = read_srt(srt_path) if srt_path else []
    caption_clips = []
    items = enhanced or srt
    for item in items:
        if enhanced:
            start, end, text = float(item["start_time"]), float(item["end_time"]), item.get("text", "")
        else:
            start, end, text = item["start"], item["end"], item["text"]
        if not text:
            continue
        img = make_caption_image(text, width, font_size, font_path=font_path)
        caption = ImageClip(img).with_start(start).with_duration(max(0.05, end - start))
        caption_clips.append(caption.with_position(("center", height - img.height - subtitle_gap)))

    final = CompositeVideoClip([timeline, *caption_clips], size=(width, height)).with_duration(total)
    if audio:
        final = final.with_audio(audio)

    output = str(output)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    final.write_videofile(
        output,
        fps=int(spec.get("fps", 30)),
        codec=spec.get("codec", "libx264"),
        audio_codec="aac",
        bitrate=spec.get("bitrate", "8000k"),
        audio_bitrate=spec.get("audio_bitrate", "256k"),
        preset=spec.get("preset", "medium"),
        ffmpeg_params=["-crf", str(spec.get("crf", 18)), "-movflags", "+faststart"],
    )
    return output

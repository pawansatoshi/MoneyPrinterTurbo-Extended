"""Forensic QC helpers: sample rendered frames and audio with FFmpeg/FFprobe.

These checks are intentionally conservative. They detect objective failures;
AI/CV/ASR providers can enrich the same report without turning unavailable
analysis into a pass.
"""
from __future__ import annotations
import json, math, subprocess, tempfile
from pathlib import Path


def probe(path: str) -> dict:
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path], text=True))


def _frames(path: str, out: Path, fps: float = .5) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    pattern = str(out / "frame_%05d.jpg")
    subprocess.run(["ffmpeg","-y","-i",path,"-vf",f"fps={fps}","-q:v","3",pattern], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted(out.glob("frame_*.jpg"))


def run(path: str, sample_fps: float = .5) -> dict:
    p = probe(path)
    video = next((s for s in p.get("streams",[]) if s.get("codec_type")=="video"), None)
    audio = next((s for s in p.get("streams",[]) if s.get("codec_type")=="audio"), None)
    result = {"available": True, "checks": {}, "warnings": [], "blocking_repairs": []}
    if not video:
        result["checks"]["video_stream"] = False; result["blocking_repairs"].append("repair_visual_integrity"); return result
    result["checks"]["video_stream"] = True
    result["checks"]["audio_present"] = audio is not None
    if audio is None: result["blocking_repairs"].append("repair_audio_quality")
    try:
        with tempfile.TemporaryDirectory() as td:
            frames = _frames(path, Path(td), sample_fps)
            result["checks"]["sampled_frames"] = len(frames) > 0
            if not frames: result["blocking_repairs"].append("repair_visual_integrity")
            # Black-frame detection via ffmpeg blackdetect over the full file.
            proc = subprocess.run(["ffmpeg","-hide_banner","-i",path,"-vf","blackdetect=d=0.75:pix_th=0.98","-an","-f","null","-"],capture_output=True,text=True)
            black = "black_start:" in (proc.stderr or "")
            result["checks"]["no_long_black_frames"] = not black
            if black: result["blocking_repairs"].append("repair_visual_integrity")
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        result["available"] = False; result["warnings"].append(f"forensic tools unavailable: {exc}")
    result["pass"] = result["available"] and all(result["checks"].values())
    return result

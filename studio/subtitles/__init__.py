"""Subtitle style registry for Pawan Video Studio."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PRESETS_PATH = ROOT / "presets.json"


def load_presets() -> dict[str, Any]:
    return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))


def list_styles() -> list[str]:
    return list(load_presets().get("styles", {}).keys())


def get_style(name: str, aspect_ratio: str | None = None) -> dict[str, Any]:
    data = load_presets()
    style = dict(data.get("styles", {}).get(name, data["styles"]["clean"]))
    if aspect_ratio and aspect_ratio in data.get("formats", {}):
        style["safe_area"] = data["formats"][aspect_ratio]
    style["name"] = name
    return style


__all__ = ["get_style", "list_styles", "load_presets"]

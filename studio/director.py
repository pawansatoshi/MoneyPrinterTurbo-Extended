"""Master Director: turns a creative brief into a deterministic Studio manifest.

The director deliberately separates *claims* from *creative treatment*. Product
facts are never invented; supplied authentic assets are marked as such and
conceptual/AI footage is explicitly labelled.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

CAMERAS = ("push_in","pull_out","pan_left","pan_right","pan_up","pan_down",
           "drift_left","drift_right","drift_up","drift_down","center")
TEMPLATES = {"launch": ["hook","problem","proof","product","why_now","cta"],
             "explainer": ["hook","context","mechanism","example","takeaway","cta"],
             "demo": ["hook","setup","demo","proof","result","cta"],
             "announcement": ["hook","announcement","proof","details","why_now","cta"],
             "comparison": ["hook","baseline","contrast","evidence","verdict","cta"],
             "documentary": ["hook","context","tension","discovery","meaning","cta"]}

@dataclass
class Shot:
    id: str
    beat: str
    narration: str
    asset: str
    source_type: str = "conceptual"
    camera: str = "auto"
    transition: str = "fade"
    overlay: str | None = None
    duration: float = 4.0
    evidence_ids: list[str] | None = None

class MasterDirector:
    """Reusable planning brain with deterministic output and safe defaults."""
    def __init__(self, seed: int = 42):
        self.seed = seed

    def _pick_camera(self, index: int) -> str:
        return CAMERAS[(self.seed + index * 7) % len(CAMERAS)]

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]{3,}", text.lower()))

    def match_assets(self, text: str, assets: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not assets:
            return None
        wanted = self._tokens(text)
        ranked = []
        for asset in assets:
            hay = self._tokens(" ".join(str(asset.get(k, "")) for k in ("name","description","tags","keywords")))
            score = len(wanted & hay)
            ranked.append((score, bool(asset.get("authentic")), asset))
        ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return ranked[0][2]

    def plan(self, brief: dict[str, Any]) -> dict[str, Any]:
        topic = str(brief.get("topic", "Untitled project"))
        script = str(brief.get("script", ""))
        template = str(brief.get("template", "explainer")).lower()
        beats = TEMPLATES.get(template, TEMPLATES["explainer"])
        paragraphs = [p.strip() for p in re.split(r"(?<=[.!?])\s+", script) if p.strip()]
        assets = list(brief.get("assets", []))
        shots: list[dict[str, Any]] = []
        for i, beat in enumerate(beats):
            text = paragraphs[min(i, len(paragraphs)-1)] if paragraphs else f"{beat}: {topic}"
            match = self.match_assets(text, assets)
            asset_path = match.get("path") if match else brief.get("fallback_asset", "")
            source_type = "authentic" if match and match.get("authentic") else (match.get("source_type", "conceptual") if match else "conceptual")
            shots.append(asdict(Shot(
                id=f"shot-{i+1:02d}", beat=beat, narration=text, asset=asset_path,
                source_type=source_type, camera=self._pick_camera(i),
                transition="cut" if beat in {"hook","cta"} else "fade",
                overlay=beat if brief.get("show_beat_labels") else None,
                duration=float(brief.get("scene_duration", 4.0)),
                evidence_ids=list(match.get("evidence_ids", [])) if match else [])))
        return {
            "studio_version": 2,
            "project": brief.get("project", topic.lower().replace(" ", "-")[:64]),
            "topic": topic,
            "template": template,
            "seed": self.seed,
            "resolution": brief.get("resolution", [1080, 1920]),
            "fps": int(brief.get("fps", 30)),
            "shots": shots,
            "scenes": [{"asset": s["asset"], "duration": s["duration"], "camera": s["camera"],
                        "transition": s["transition"], "overlay": s["overlay"]} for s in shots if s["asset"]],
            "authentic_asset_policy": "never_invent_product_state",
            "sources": brief.get("sources", []),
            "brand": brief.get("brand", {}),
            "subtitles": brief.get("subtitles", {"font_size": 54, "bottom_margin": 120}),
            "audio": brief.get("audio"),
            "subtitle": brief.get("subtitle"),
            "enhanced_subtitle": brief.get("enhanced_subtitle"),
            "metadata": {"title_options": brief.get("title_options", []),
                         "description": brief.get("description", ""),
                         "hashtags": brief.get("hashtags", [])}
        }

    def save(self, manifest: dict[str, Any], path: str | Path) -> str:
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(p)

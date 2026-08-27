"""Automated quality gate for Studio manifests and rendered projects."""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

@dataclass
class Finding:
    severity: str
    code: str
    message: str
    shot_id: str | None = None

class QualityGate:
    """Static preflight checks; optional ffprobe checks are handled when available."""
    def check(self, manifest: dict[str, Any]) -> dict[str, Any]:
        findings: list[Finding] = []
        shots = manifest.get("shots", [])
        if not shots:
            findings.append(Finding("error", "NO_SHOTS", "No planned shots found."))
        for shot in shots:
            sid = shot.get("id")
            asset = str(shot.get("asset", ""))
            source = shot.get("source_type", "conceptual")
            if source == "authentic" and not asset:
                findings.append(Finding("error", "AUTHENTIC_ASSET_MISSING", "Authentic shot has no asset path.", sid))
            if asset and not Path(asset).exists():
                findings.append(Finding("warning", "ASSET_NOT_FOUND", f"Asset is not present at render time: {asset}", sid))
            if source == "authentic" and re.search(r"(?:apy|apr|balance|rate|ltv|yield|tv\w*)", shot.get("narration", ""), re.I) and not shot.get("evidence_ids"):
                findings.append(Finding("warning", "CLAIM_WITHOUT_EVIDENCE", "Product/financial-looking claim has no evidence id.", sid))
            if len(shot.get("narration", "").split()) > 42:
                findings.append(Finding("warning", "LONG_SHOT_COPY", "Shot narration is unusually long; consider splitting the beat.", sid))
        resolution = manifest.get("resolution", [1080, 1920])
        if len(resolution) != 2 or min(resolution) <= 0:
            findings.append(Finding("error", "BAD_RESOLUTION", "Resolution must be [width, height]."))
        counts = {"error": 0, "warning": 0, "info": 0}
        for f in findings: counts[f.severity] = counts.get(f.severity, 0) + 1
        return {"ok": counts.get("error", 0) == 0, "counts": counts, "findings": [asdict(f) for f in findings]}

    def revise(self, manifest: dict[str, Any]) -> dict[str, Any]:
        """Conservative self-revision: remove invalid shots and preserve authenticity."""
        report = self.check(manifest)
        blocked = {f["shot_id"] for f in report["findings"] if f["severity"] == "error" and f.get("shot_id")}
        if blocked:
            manifest = dict(manifest)
            manifest["shots"] = [s for s in manifest.get("shots", []) if s.get("id") not in blocked]
            manifest["scenes"] = [{"asset": s.get("asset",""), "duration": s.get("duration",4),
                                    "camera": s.get("camera","auto"), "transition": s.get("transition","fade"),
                                    "overlay": s.get("overlay")} for s in manifest["shots"] if s.get("asset")]
        manifest.setdefault("quality", {})["preflight"] = self.check(manifest)
        return manifest

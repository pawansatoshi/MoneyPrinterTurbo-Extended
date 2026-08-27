"""Manifest preflight checks before an expensive render."""
from __future__ import annotations

import json
from pathlib import Path

ALLOWED_FORMATS = {"16:9": (16, 9), "9:16": (9, 16), "1:1": (1, 1)}


def run(manifest: str | Path) -> dict:
    p = Path(manifest)
    spec = json.loads(p.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    fmt = spec.get("format", "16:9")
    if fmt not in ALLOWED_FORMATS:
        errors.append(f"Unsupported format: {fmt}")
    resolution = spec.get("resolution", [1920, 1080])
    if len(resolution) != 2 or min(resolution) <= 0:
        errors.append("Invalid resolution")
    if fmt == "16:9" and resolution[0] / resolution[1] < 1.7:
        errors.append("16:9 manifest has incompatible resolution")
    if fmt == "9:16" and resolution[0] / resolution[1] > 0.65:
        errors.append("9:16 manifest has incompatible resolution")
    if fmt == "1:1" and abs(resolution[0] / resolution[1] - 1) > 0.02:
        errors.append("1:1 manifest has incompatible resolution")

    scenes = spec.get("scenes", [])
    if not scenes:
        errors.append("No scenes configured")
    for i, scene in enumerate(scenes):
        asset = scene.get("asset")
        if not asset:
            errors.append(f"Scene {i + 1}: missing asset")
        elif not Path(asset).exists():
            warnings.append(f"Scene {i + 1}: asset is not mounted yet: {asset}")

    quality = spec.get("quality", {})
    if quality.get("require_asset_provenance", True):
        for i, asset in enumerate(spec.get("assets", [])):
            for field in ("source", "license"):
                if not asset.get(field):
                    errors.append(f"Asset {i + 1}: missing {field}")
    if quality.get("require_source_claims", True) and spec.get("project", {}).get("claims_policy") == "official_only":
        warnings.append("Claims policy is official_only: research/source records must accompany factual copy")

    result = {"manifest": str(p), "errors": errors, "warnings": warnings, "render_ready": not errors}
    return result


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Studio manifest preflight")
    ap.add_argument("manifest")
    args = ap.parse_args()
    print(json.dumps(run(args.manifest), indent=2))

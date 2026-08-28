"""Free-first PawanStudio GitHub Actions entry point.

This runner is intentionally fail-closed. It orchestrates the repository's
existing studio modules when available and writes auditable manifests. It does
not fabricate official project assets or silently substitute a voice.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "current"
OUT.mkdir(parents=True, exist_ok=True)


def fail(msg: str) -> None:
    report = {"status": "BLOCKED", "reason": msg}
    (OUT / "qc_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"BLOCKED: {msg}")
    raise SystemExit(2)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--project-url", required=True)
    p.add_argument("--language", required=True)
    p.add_argument("--aspect-ratio", required=True)
    p.add_argument("--style", required=True)
    p.add_argument("--duration", required=True)
    p.add_argument("--free-mode", action="store_true")
    a = p.parse_args()

    parsed = urlparse(a.project_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fail("project_url must be an HTTP(S) official source")

    # Keep all job intent auditable before invoking the renderer.
    request = {
        "project_url": a.project_url,
        "language": a.language,
        "aspect_ratio": a.aspect_ratio,
        "style": a.style,
        "duration_seconds": int(a.duration),
        "free_mode": bool(a.free_mode),
        "fail_closed": os.getenv("PAWANSTUDIO_FAIL_CLOSED") == "true",
    }
    (OUT / "request.json").write_text(json.dumps(request, indent=2), encoding="utf-8")

    # Do not claim a complete render when the repository has not exposed its
    # production engine entry point. This makes the GitHub Action honest.
    candidates = [
        ROOT / "studio" / "engine.py",
        ROOT / "studio" / "pipeline.py",
        ROOT / "studio" / "production" / "pipeline.py",
    ]
    engine = next((x for x in candidates if x.exists()), None)
    if engine is None:
        fail("No production-engine entry point found; connect the existing studio renderer before rendering")

    # Existing engine contracts vary across forks. Never guess CLI arguments.
    # A future adapter can be added here once the repository exposes a stable
    # callable/CLI contract. Until then, fail closed instead of generating a
    # misleading or unverified video.
    fail(f"Production adapter for {engine.relative_to(ROOT)} is not declared")


if __name__ == "__main__":
    main()

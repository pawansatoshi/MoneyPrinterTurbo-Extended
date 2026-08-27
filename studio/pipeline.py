"""Single-command orchestration for the reusable Studio pipeline.

The pipeline keeps project data separate from production logic: preflight ->
optional planning -> render -> technical QC. External media/TTS providers are
adapters and never required for the core renderer.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .creative.planner import plan
from .qc.preflight import run as preflight


def prepare(manifest: str | Path, plan_output: str | Path | None = None) -> dict:
    spec = json.loads(Path(manifest).read_text(encoding="utf-8"))
    result = preflight(manifest)
    if not result["render_ready"]:
        return result
    production_plan = plan(spec)
    if plan_output:
        Path(plan_output).parent.mkdir(parents=True, exist_ok=True)
        Path(plan_output).write_text(json.dumps(production_plan, indent=2), encoding="utf-8")
    result["production_plan"] = production_plan
    return result


def render(manifest: str | Path, output: str | Path) -> dict:
    check = prepare(manifest)
    if not check["render_ready"]:
        raise RuntimeError(json.dumps(check, indent=2))
    subprocess.run([sys.executable, "-m", "studio.render", str(manifest), "--output", str(output)], check=True)
    fmt = json.loads(Path(manifest).read_text(encoding="utf-8")).get("format", "16:9")
    qc = subprocess.run([sys.executable, "-m", "studio.qc.check", str(output), "--format", fmt], capture_output=True, text=True)
    report = json.loads(qc.stdout) if qc.stdout.strip() else {"master_ready": False, "error": qc.stderr}
    return {"preflight": check, "output": str(output), "qc": report}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Pawan Video Studio production pipeline")
    ap.add_argument("manifest")
    ap.add_argument("--output", required=True)
    ap.add_argument("--plan", default=None)
    args = ap.parse_args()
    result = render(args.manifest, args.output)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result.get("qc", {}).get("master_ready") else 2)

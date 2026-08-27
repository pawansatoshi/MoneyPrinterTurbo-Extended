"""Durable, JSON-compatible checkpoints for resumable production."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

class CheckpointStore:
    def __init__(self, root: str | Path):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def save(self, project: str, stage: str, state: dict[str, Any]) -> str:
        path = self.root / f"{project}.json"
        payload = {"project": project, "stage": stage, "updated_at": datetime.now(timezone.utc).isoformat(), "state": state}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)
    def load(self, project: str) -> dict[str, Any] | None:
        path = self.root / f"{project}.json"
        if not path.exists(): return None
        return json.loads(path.read_text(encoding="utf-8"))

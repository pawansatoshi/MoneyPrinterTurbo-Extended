"""Provider-neutral agentic production state machine.

This is the orchestration contract: reasoning/research/media providers are
injected, state is checkpointed, and a stage cannot be marked complete merely
because an adapter was requested.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Callable

STAGES = ["discover","research","evidence","thesis","story","differentiate","visual_language","storyboard","assets","voice","captions","motion","audio","timeline","render","review","heal","export"]

@dataclass
class StageState:
    name: str
    status: str = "pending"
    attempts: int = 0
    output: dict[str, Any] | None = None
    error: str | None = None
    updated_at: str = ""

class ProductionBrain:
    def __init__(self, state_path: str | Path):
        self.path = Path(state_path)
        self.state = {"version": 1, "stages": {s: asdict(StageState(s, updated_at=self._now())) for s in STAGES}}
        if self.path.exists(): self.state = json.loads(self.path.read_text(encoding="utf-8"))

    def _now(self): return datetime.now(timezone.utc).isoformat()
    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True); self.path.write_text(json.dumps(self.state, indent=2), encoding="utf-8")
    def checkpoint(self, stage: str, status: str, output: dict[str, Any] | None = None, error: str | None = None):
        item=self.state["stages"][stage]; item.update(status=status, output=output, error=error, updated_at=self._now()); item["attempts"] += 1; self.save()
    def resume_from(self) -> str | None:
        for s in STAGES:
            if self.state["stages"][s]["status"] != "passed": return s
        return None
    def run(self, workers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]], context: dict[str, Any]) -> dict[str, Any]:
        for stage in STAGES:
            item=self.state["stages"][stage]
            if item["status"] == "passed": continue
            worker=workers.get(stage)
            if worker is None:
                self.checkpoint(stage,"blocked",error="No executable worker registered")
                break
            self.checkpoint(stage,"running")
            try:
                result=worker(context)
                if not result.get("ready", True):
                    self.checkpoint(stage,"blocked",result,result.get("error","worker did not pass")); break
                context.update(result.get("context",{})); self.checkpoint(stage,"passed",result)
            except Exception as exc:
                self.checkpoint(stage,"failed",error=str(exc)); break
        return self.state

"""Self-healing controller for PawanStudio.

The controller never pretends that missing analysis passed. It applies only
explicit remediation callbacks supplied by the production runtime and stops
on convergence or a configurable retry budget.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class HealingResult:
    status: str
    attempts: int
    history: list[dict[str, Any]]


def heal(initial: dict[str, Any], repairers: dict[str, Callable[[], Any]],
         evaluate: Callable[[], dict[str, Any]], max_attempts: int = 3) -> HealingResult:
    state = initial
    history = [{"attempt": 0, "qc": state}]
    for attempt in range(1, max_attempts + 1):
        repairs = state.get("blocking_repairs", [])
        if not repairs and state.get("master_ready") is True:
            return HealingResult("pass", attempt - 1, history)
        applied = []
        for repair in repairs:
            fn = repairers.get(repair)
            if fn is None:
                continue
            fn()
            applied.append(repair)
        if not applied:
            return HealingResult("blocked", attempt - 1, history)
        state = evaluate()
        history.append({"attempt": attempt, "applied": applied, "qc": state})
        if state.get("master_ready") is True:
            return HealingResult("pass", attempt, history)
    return HealingResult("needs_review", max_attempts, history)

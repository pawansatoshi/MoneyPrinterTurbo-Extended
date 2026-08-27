"""Evaluate whether a production run has completed the studio contract."""
from pathlib import Path
from typing import Mapping
from .production_contract import ProductionContract


def evaluate(completed: set[str]) -> Mapping[str, object]:
    contract = ProductionContract()
    gates = contract.validate(completed)
    return {
        "ready": contract.ready(completed),
        "passed": [g.stage for g in gates if g.passed],
        "blocked": [g.stage for g in gates if not g.passed],
        "blocking_reasons": [reason for g in gates for reason in g.blocking],
    }

"""Dependency-light advanced QC gates and machine-readable remediation hints.

Heavy CV/ASR providers plug into these contracts. No provider result is
invented: unavailable analyses are reported as unavailable, not passed.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class Gate:
    name: str
    passed: bool
    severity: str
    reason: str
    repair: str

REQUIRED = (
    "identity_provenance", "product_authenticity", "claim_evidence",
    "visual_integrity", "audio_quality", "subtitle_quality",
    "story_retention", "asset_provenance", "platform_compliance"
)


def evaluate(results: dict[str, Any], *, require_all: bool = True) -> dict[str, Any]:
    gates = []
    for name in REQUIRED:
        value = results.get(name)
        if value is True:
            gates.append(Gate(name, True, "info", "passed", "none"))
        elif value is False:
            gates.append(Gate(name, False, "blocking", "failed", f"repair_{name}"))
        else:
            gates.append(Gate(name, False if require_all else True, "blocking" if require_all else "warning", "analysis unavailable", f"run_{name}"))
    passed = all(g.passed for g in gates)
    return {"master_ready": passed, "gates": [asdict(g) for g in gates],
            "blocking_repairs": [g.repair for g in gates if not g.passed]}


def validate_claims(claims: list[dict]) -> list[str]:
    errors = []
    for i, claim in enumerate(claims):
        if not claim.get("claim"):
            errors.append(f"claim {i+1}: missing text")
        if not claim.get("evidence"):
            errors.append(f"claim {i+1}: missing evidence")
    return errors


def validate_assets(assets: list[dict]) -> list[str]:
    errors = []
    for i, asset in enumerate(assets):
        if not asset.get("source"):
            errors.append(f"asset {i+1}: missing source")
        if not asset.get("provenance"):
            errors.append(f"asset {i+1}: missing provenance")
        if asset.get("product_claim") and not asset.get("official_verified"):
            errors.append(f"asset {i+1}: product asset is not officially verified")
    return errors

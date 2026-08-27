"""Provider-neutral research contract for autonomous project discovery.

A runtime browser/search adapter supplies live results. This layer enforces
source priority and freshness requirements before facts enter production.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

@dataclass(frozen=True)
class ResearchItem:
    url: str
    title: str
    source_type: str
    official: bool
    retrieved_at: str
    published_at: str | None = None
    evidence: str = ""

PRIORITY = {"official_docs": 1.0, "official_website": .98, "official_blog": .96,
            "official_github": .94, "official_social": .92, "primary_data": .90,
            "independent": .70, "secondary": .50}


def rank(items: Iterable[ResearchItem]) -> list[dict]:
    rows = []
    for item in items:
        score = PRIORITY.get(item.source_type, .3)
        if item.official: score = min(1.0, score + .03)
        rows.append({**asdict(item), "priority": score})
    return sorted(rows, key=lambda x: x["priority"], reverse=True)


def factual_claim_allowed(claim: dict, *, current: bool = False) -> bool:
    """Block claims without evidence; current claims also require freshness."""
    if not claim.get("evidence"): return False
    if current and not claim.get("verified_at"): return False
    return float(claim.get("confidence", 0)) >= .75

"""Project-specific originality and anti-cliche scoring for PawanStudio.

This module is deterministic and provider-neutral. A research/LLM adapter can
supply candidate concepts and observed competitor patterns; this layer scores
and filters them before production.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import re
from typing import Iterable

GENERIC_PATTERNS = [
    r"welcome to", r"in this video", r"the future of", r"revolutionary",
    r"game[- ]changer", r"you won't believe", r"wait until the end",
    r"everything you need to know", r"what is .*\?"
]

@dataclass(frozen=True)
class Concept:
    title: str
    hook: str
    angle: str
    visual_device: str
    novelty: float
    evidence_fit: float
    visual_fit: float
    retention_fit: float
    cliché_penalty: float
    score: float


def cliché_score(text: str) -> float:
    hits = sum(bool(re.search(p, text, re.I)) for p in GENERIC_PATTERNS)
    return min(1.0, hits / 2.0)


def score_concept(title: str, hook: str, angle: str, visual_device: str,
                  novelty: float = .5, evidence_fit: float = .7,
                  visual_fit: float = .7, retention_fit: float = .7) -> Concept:
    penalty = cliché_score(f"{title} {hook} {angle}")
    score = max(0.0, min(1.0,
        .30 * novelty + .20 * evidence_fit + .20 * visual_fit +
        .20 * retention_fit + .10 * (1.0 - penalty)))
    return Concept(title, hook, angle, visual_device, novelty, evidence_fit,
                   visual_fit, retention_fit, penalty, score)


def rank(concepts: Iterable[dict]) -> list[dict]:
    scored = []
    for c in concepts:
        scored.append(asdict(score_concept(
            c.get("title", ""), c.get("hook", ""), c.get("angle", ""),
            c.get("visual_device", ""), float(c.get("novelty", .5)),
            float(c.get("evidence_fit", .7)), float(c.get("visual_fit", .7)),
            float(c.get("retention_fit", .7)))))
    return sorted(scored, key=lambda x: x["score"], reverse=True)


def needs_rework(concept: dict, threshold: float = .60) -> bool:
    return float(concept.get("score", 0)) < threshold or float(concept.get("cliché_penalty", 0)) >= .5

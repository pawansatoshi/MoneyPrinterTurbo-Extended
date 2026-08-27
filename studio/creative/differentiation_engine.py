"""Creative differentiation primitives.

Turns a project brief and known research signals into auditable creative concepts.
This module deliberately does not claim to predict virality; it scores originality
signals and flags common/cliche treatments for a higher-level director to review.
"""
from dataclasses import dataclass, field
from typing import Iterable, List
import re

@dataclass
class Concept:
    title: str
    hook: str
    angle: str
    visual_language: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    scores: dict = field(default_factory=dict)

class DifferentiationEngine:
    def __init__(self, common_patterns: Iterable[str] | None = None):
        self.common_patterns = [re.compile(p, re.I) for p in (common_patterns or [
            r"what is .+", r"everything you need to know", r"ultimate guide",
            r"the future of .+", r"you won't believe", r"wait until the end"
        ])]

    def score(self, concept: Concept) -> Concept:
        text = f"{concept.title} {concept.hook} {concept.angle}".lower()
        cliches = sum(bool(p.search(text)) for p in self.common_patterns)
        specificity = min(1.0, (len(set(re.findall(r"[a-z0-9]+", text))) / 35))
        visual = min(1.0, len(concept.visual_language) / 5)
        concept.scores = {
            "originality_signal": round(max(0.0, 1 - cliches * .22), 3),
            "specificity": round(specificity, 3),
            "visual_potential": round(visual, 3),
            "overall": round(max(0.0, (1 - cliches*.22)*.45 + specificity*.25 + visual*.30), 3),
        }
        if cliches:
            concept.risks.append("generic_or_cliche_packaging")
        return concept

    def rank(self, concepts: Iterable[Concept]) -> list[Concept]:
        return sorted((self.score(c) for c in concepts), key=lambda c: c.scores["overall"], reverse=True)

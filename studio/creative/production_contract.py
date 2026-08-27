"""Production contract: capabilities are explicit and testable, not marketing claims."""
from dataclasses import dataclass, field
from typing import List

REQUIRED_STAGES = [
    "brief", "project_memory", "research", "evidence", "thesis", "story",
    "creative_differentiation", "visual_language", "storyboard", "shot_plan",
    "assets", "voice", "captions", "motion_graphics", "audio", "timeline",
    "render", "multimodal_review", "revision", "platform_exports"
]

@dataclass
class ProductionGate:
    stage: str
    passed: bool
    blocking: List[str] = field(default_factory=list)

class ProductionContract:
    def validate(self, completed: set[str]) -> list[ProductionGate]:
        return [ProductionGate(s, s in completed, [] if s in completed else [f"missing:{s}"])
                for s in REQUIRED_STAGES]

    def ready(self, completed: set[str]) -> bool:
        return all(g.passed for g in self.validate(completed))

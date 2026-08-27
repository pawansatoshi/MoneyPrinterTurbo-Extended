"""Provider selection independent of any one AI vendor."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

@dataclass(frozen=True)
class Provider:
    name: str
    capability: str
    quality: float = 0.5
    control: float = 0.5
    reliability: float = 0.5
    cost_efficiency: float = 0.5
    latency: float = 0.5
    continuity: float = 0.5
    local: bool = False
    enabled: bool = True

class ProviderRouter:
    """Rank providers by task fit and operating constraints; never hard-code a vendor."""
    def __init__(self, providers: Iterable[Provider] = ()):
        self.providers = list(providers)

    def rank(self, capability: str, *, prefer_local: bool=False, min_quality: float=0.0) -> list[dict]:
        candidates = [p for p in self.providers if p.enabled and p.capability == capability and p.quality >= min_quality]
        def score(p: Provider) -> float:
            s = (p.quality*0.28 + p.control*0.14 + p.reliability*0.16 +
                 p.cost_efficiency*0.16 + p.latency*0.10 + p.continuity*0.16)
            if prefer_local and p.local: s += 0.08
            return s
        return [{**asdict(p), "score": round(score(p), 4)} for p in sorted(candidates, key=score, reverse=True)]

    def choose(self, capability: str, **kwargs) -> dict | None:
        ranked = self.rank(capability, **kwargs)
        return ranked[0] if ranked else None

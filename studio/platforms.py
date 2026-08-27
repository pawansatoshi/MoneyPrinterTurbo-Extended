"""Output profiles and repurposing rules for YouTube, Shorts/Reels and LinkedIn."""
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class OutputProfile:
    name: str
    width: int
    height: int
    fps: int
    max_seconds: int | None
    safe_top: float
    safe_bottom: float

PROFILES={
 "youtube":OutputProfile("youtube",1920,1080,30,None,.07,.10),
 "shorts":OutputProfile("shorts",1080,1920,30,180,.10,.18),
 "reels":OutputProfile("reels",1080,1920,30,180,.10,.18),
 "linkedin":OutputProfile("linkedin",1080,1350,30,600,.08,.12),
}

def profile(name:str)->dict:
    if name not in PROFILES: raise ValueError(f"Unknown output profile: {name}")
    return asdict(PROFILES[name])

def all_profiles()->list[dict]: return [asdict(x) for x in PROFILES.values()]

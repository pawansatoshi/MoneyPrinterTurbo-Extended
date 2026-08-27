"""Persistent, project-scoped knowledge contract for PawanStudio."""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any

@dataclass
class ProjectMemory:
    project_name: str
    official_sources: list[dict[str, Any]] = field(default_factory=list)
    claims: list[dict[str, Any]] = field(default_factory=list)
    assets: list[dict[str, Any]] = field(default_factory=list)
    approved_constraints: dict[str, Any] = field(default_factory=dict)
    last_refresh: str = ""
    refresh_version: int = 0

    def refresh(self, official_sources: list[dict[str, Any]], claims: list[dict[str, Any]],
                assets: list[dict[str, Any]]) -> None:
        self.official_sources = official_sources
        self.claims = claims
        self.assets = assets
        self.last_refresh = datetime.now(timezone.utc).isoformat()
        self.refresh_version += 1

    def snapshot(self) -> dict[str, Any]:
        return asdict(self)

    def verified_source_urls(self) -> list[str]:
        return [s["url"] for s in self.official_sources if s.get("verified")]

    def official_assets(self) -> list[dict[str, Any]]:
        return [a for a in self.assets if a.get("official") and a.get("verified")]


def needs_refresh(memory: ProjectMemory, max_age_hours: int = 24) -> bool:
    if not memory.last_refresh:
        return True
    try:
        then = datetime.fromisoformat(memory.last_refresh)
        age = datetime.now(timezone.utc) - then
        return age.total_seconds() >= max_age_hours * 3600
    except ValueError:
        return True

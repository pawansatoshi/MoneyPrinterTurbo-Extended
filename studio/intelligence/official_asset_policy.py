"""Authentic asset selection and provenance rules."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional

@dataclass(frozen=True)
class AssetRecord:
    asset_id: str
    project: str
    kind: str
    url: str
    source_url: str
    source_type: str
    official: bool
    verified: bool
    license: Optional[str] = None
    retrieved_at: str = ""

    def __post_init__(self):
        if not self.retrieved_at:
            object.__setattr__(self, "retrieved_at", datetime.now(timezone.utc).isoformat())


def choose_asset(kind: str, records: list[AssetRecord], require_official: bool = False) -> Optional[AssetRecord]:
    candidates = [r for r in records if r.kind == kind and r.verified]
    if require_official:
        candidates = [r for r in candidates if r.official]
    # Official verified assets always outrank generated/decorative assets.
    candidates.sort(key=lambda r: (r.official, r.source_type == "website", r.verified), reverse=True)
    return candidates[0] if candidates else None


def authenticity_gate(asset: AssetRecord, product_claim: bool) -> tuple[bool, str]:
    if product_claim and not asset.official:
        return False, "Product proof must use a verified official asset."
    if not asset.verified:
        return False, "Asset provenance is not verified."
    return True, "ok"


def serialize_asset_vault(records: list[AssetRecord]) -> dict:
    return {
        "version": 1,
        "policy": "official product assets outrank generated media",
        "assets": [asdict(r) for r in records],
    }

"""Creator identity provenance policy for photos, video and voice.

Only user-supplied or explicitly authorized identity media may be used as the
creator. Synthetic substitutions are blocked unless the project explicitly
opts into them and records authorization.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class CreatorAsset:
    path: str
    media_type: str
    source: str
    authorized: bool
    synthetic: bool = False
    consent_reference: str | None = None


def validate(asset: CreatorAsset) -> dict:
    errors = []
    if not asset.path: errors.append("missing asset path")
    if not asset.source: errors.append("missing source provenance")
    if not asset.authorized: errors.append("creator asset is not authorized")
    if asset.synthetic and not asset.consent_reference:
        errors.append("synthetic creator asset requires explicit consent reference")
    return {"pass": not errors, "errors": errors, "asset": asdict(asset)}


def policy() -> dict:
    return {
        "default": "original_authorized_only",
        "silent_synthetic_substitution": False,
        "voice_clone_requires_consent": True,
        "face_generation_requires_explicit_opt_in": True,
    }

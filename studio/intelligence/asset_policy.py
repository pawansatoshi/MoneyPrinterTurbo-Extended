"""Deterministic asset-selection rules used by the creative director."""
from __future__ import annotations

from typing import Any


def rank_asset(asset: dict[str, Any], purpose: str) -> tuple[int, int]:
    source = asset.get("source", "").lower()
    typ = asset.get("asset_type", "").lower()
    score = 0
    if source == "official_website":
        score += 100
    if purpose in {"logo", "brand", "product_ui", "announcement", "proof"} and source == "official_website":
        score += 100
    if purpose in {"logo", "brand"} and "brand_logo" in typ:
        score += 50
    if purpose == "product_ui" and typ in {"image", "video"}:
        score += 25
    if asset.get("page_url"):
        score += 5
    return (-score, len(asset.get("url", "")))


def select_asset(assets: list[dict[str, Any]], purpose: str) -> dict[str, Any] | None:
    candidates = [a for a in assets if a.get("source") == "official_website"] if purpose in {"logo", "brand", "product_ui", "proof"} else assets
    return sorted(candidates, key=lambda a: rank_asset(a, purpose))[0] if candidates else None


def assert_authentic_product_asset(asset: dict[str, Any]) -> None:
    if asset.get("purpose") in {"logo", "product_ui", "announcement", "proof"} and asset.get("source") != "official_website":
        raise ValueError("Official product proof must come from the configured official origin")

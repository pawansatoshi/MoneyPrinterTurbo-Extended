"""Live research runtime contracts for PawanStudio.

The runtime uses an injected browser/search adapter. It never labels a source
official merely because a domain looks plausible. Adapters must return fetched
content plus identity evidence; the verifier then applies conservative rules.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Protocol
from urllib.parse import urlparse

class ResearchAdapter(Protocol):
    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]: ...
    def fetch(self, url: str) -> dict[str, Any]: ...

@dataclass(frozen=True)
class ResearchRecord:
    url: str
    title: str
    source_type: str
    fetched_at: str
    identity_signals: list[str]
    confidence: float
    verified_official: bool
    evidence: dict[str, Any]


def _same_site(a: str, b: str) -> bool:
    return urlparse(a).netloc.lower().removeprefix("www.") == urlparse(b).netloc.lower().removeprefix("www.")


def verify_candidate(project_name: str, candidate: dict[str, Any], fetched: dict[str, Any], seed_url: str | None = None) -> ResearchRecord:
    url = candidate.get("url", "")
    text = str(fetched.get("text", ""))
    title = str(fetched.get("title") or candidate.get("title") or "")
    signals: list[str] = []
    if seed_url and _same_site(url, seed_url): signals.append("same-origin-as-user-seed")
    if project_name.lower() in (title + " " + text[:5000]).lower(): signals.append("project-name-present")
    if candidate.get("organization") and project_name.lower() in str(candidate["organization"]).lower(): signals.append("provider-identified-project")
    # Conservative: a URL alone can never make an official source.
    confidence = min(0.99, 0.45 + 0.2 * len(signals))
    verified = bool(seed_url and _same_site(url, seed_url) and "project-name-present" in signals)
    return ResearchRecord(url, title, candidate.get("source_type", "web"), datetime.now(timezone.utc).isoformat(), signals, confidence, verified, {"excerpt": text[:1200]})


def research(project_name: str, adapter: ResearchAdapter, seed_url: str | None = None, queries: list[str] | None = None, limit: int = 8) -> dict[str, Any]:
    queries = queries or [project_name, f"{project_name} official", f"{project_name} docs", f"{project_name} announcement"]
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    for q in queries:
        for item in adapter.search(q, limit=limit):
            url = item.get("url", "")
            if url and url not in seen:
                seen.add(url); candidates.append(item)
    if seed_url and seed_url not in seen:
        candidates.insert(0, {"url": seed_url, "title": project_name, "source_type": "website"})
    records = []
    for c in candidates:
        try:
            records.append(asdict(verify_candidate(project_name, c, adapter.fetch(c["url"]), seed_url)))
        except Exception as exc:
            records.append({"url": c.get("url", ""), "source_type": c.get("source_type", "web"), "verified_official": False, "error": str(exc)})
    return {"project": project_name, "generated_at": datetime.now(timezone.utc).isoformat(), "records": records, "official": [r for r in records if r.get("verified_official") is True]}

"""Official-source discovery for PawanStudio.

The project name is the normal user input. An explicit URL is optional. This
module deliberately does not fabricate an official identity: callers must
validate candidates before promoting them to authoritative sources.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable, Optional
from urllib.parse import urlparse

OFFICIAL_HOST_HINTS = (
    "www.", "docs.", "blog.", "app.", "github.com", "x.com", "twitter.com"
)

@dataclass(frozen=True)
class SourceCandidate:
    url: str
    source_type: str
    host: str
    confidence: float
    reason: str
    discovered_at: str

@dataclass(frozen=True)
class OfficialSource:
    url: str
    source_type: str
    host: str
    confidence: float
    verified: bool
    discovered_at: str


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"


def host(url: str) -> str:
    return urlparse(normalize_url(url)).netloc.lower().split(":", 1)[0]


def discover_candidates(project_name: str, seed_url: Optional[str] = None,
                         known_urls: Iterable[str] = ()) -> list[SourceCandidate]:
    """Build a deterministic candidate list from supplied/previous sources.

    Network search is intentionally delegated to the Research/Browser adapter;
    this core layer only normalizes and ranks discovered URLs.
    """
    now = datetime.now(timezone.utc).isoformat()
    urls = []
    if seed_url:
        urls.append((seed_url, "website", 0.98, "user supplied seed"))
    for u in known_urls:
        urls.append((u, "known", 0.90, "previously approved project source"))
    result: list[SourceCandidate] = []
    seen = set()
    for u, typ, conf, reason in urls:
        n = normalize_url(u)
        if not n or n in seen:
            continue
        seen.add(n)
        result.append(SourceCandidate(n, typ, host(n), conf, reason, now))
    return result


def classify_source(url: str) -> str:
    h = host(url)
    path = urlparse(normalize_url(url)).path.lower()
    if "github.com" in h:
        return "github"
    if "x.com" in h or "twitter.com" in h:
        return "official_social"
    if "/docs" in path or h.startswith("docs."):
        return "docs"
    if "/blog" in path or h.startswith("blog."):
        return "blog"
    return "website"


def promote_verified(candidate: SourceCandidate, verified: bool,
                     confidence: Optional[float] = None) -> OfficialSource:
    """Promote only after an external browser/research verifier confirms it."""
    return OfficialSource(
        url=candidate.url,
        source_type=classify_source(candidate.url),
        host=candidate.host,
        confidence=candidate.confidence if confidence is None else confidence,
        verified=bool(verified),
        discovered_at=candidate.discovered_at,
    )


def source_pack(project_name: str, sources: Iterable[OfficialSource]) -> dict:
    return {
        "project": project_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "official-first; unverified sources cannot become product-of-record",
        "sources": [asdict(s) for s in sources],
    }

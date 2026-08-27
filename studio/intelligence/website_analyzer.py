"""Official-site intelligence for PawanStudio.

The analyzer is deliberately domain-scoped: a project supplies its official
origin and optional approved paths. It discovers brand/product evidence from
the real site instead of asking the user to repeatedly upload screenshots.

It never generates or modifies official assets. Discovered assets retain their
source URL, page URL, alt text and asset type so the production planner can
prefer authentic material and expose provenance.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen


@dataclass
class OfficialAsset:
    url: str
    page_url: str
    asset_type: str
    alt: str = ""
    title: str = ""
    source: str = "official_website"
    sha256: str | None = None


@dataclass
class PageEvidence:
    url: str
    title: str
    headings: list[str]
    text: str


class _HTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.assets: list[tuple[str, str, str]] = []
        self.headings: list[str] = []
        self.title = ""
        self._tag = ""
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._tag = tag
        if tag in {"h1", "h2", "h3"}:
            self._text = []
        if tag == "title":
            self._text = []
        if tag == "a" and a.get("href"):
            self.links.append((a["href"], a.get("title", "")))
        if tag == "img" and a.get("src"):
            self.assets.append((a["src"], a.get("alt", ""), "image"))
        if tag == "source" and a.get("src"):
            self.assets.append((a["src"], a.get("title", ""), "video"))
        if tag == "video" and a.get("poster"):
            self.assets.append((a["poster"], "video poster", "image"))
        if tag == "link" and a.get("href"):
            rel = (a.get("rel") or "").lower()
            if any(x in rel for x in ("icon", "apple-touch-icon")):
                self.assets.append((a["href"], "favicon", "brand_icon"))

    def handle_endtag(self, tag):
        value = " ".join(" ".join(self._text).split()).strip()
        if tag == "title" and value:
            self.title = value
        elif tag in {"h1", "h2", "h3"} and value:
            self.headings.append(value)
        self._text = []
        self._tag = ""

    def handle_data(self, data):
        if self._tag in {"title", "h1", "h2", "h3", "p", "li"}:
            self._text.append(data)


def _fetch(url: str, timeout: int = 20) -> tuple[str, bytes]:
    req = Request(url, headers={"User-Agent": "PawanStudio/2.0 official-site-analyzer"})
    with urlopen(req, timeout=timeout) as r:
        return r.headers.get("content-type", ""), r.read()


def _same_origin(url: str, origin: str) -> bool:
    return urlparse(url).netloc == urlparse(origin).netloc


def _normalize(url: str, base: str) -> str | None:
    absolute = urldefrag(urljoin(base, url))[0]
    if not absolute.startswith(("http://", "https://")):
        return None
    return absolute.rstrip("/")


def _asset_type(url: str, hint: str = "image") -> str:
    p = urlparse(url).path.lower()
    if p.endswith(".svg"):
        return "brand_logo_or_vector"
    if p.endswith((".png", ".jpg", ".jpeg", ".webp", ".avif")):
        return "image"
    if p.endswith((".mp4", ".webm", ".mov")):
        return "video"
    return hint


def analyze_official_site(origin: str, max_pages: int = 40, allowed_paths: list[str] | None = None) -> dict:
    """Crawl only the supplied official origin and return a reusable evidence/asset pack."""
    origin = origin.rstrip("/")
    queue = [origin]
    seen: set[str] = set()
    pages: list[PageEvidence] = []
    assets: dict[str, OfficialAsset] = {}
    allow = tuple(allowed_paths or ("/",))

    while queue and len(seen) < max_pages:
        url = queue.pop(0)
        if url in seen or not _same_origin(url, origin):
            continue
        path = urlparse(url).path or "/"
        if allow and not any(path == p or path.startswith(p.rstrip("/") + "/") for p in allow):
            continue
        seen.add(url)
        try:
            content_type, body = _fetch(url)
        except Exception:
            continue
        if "text/html" not in content_type and not url.endswith("/"):
            continue
        parser = _HTML()
        parser.feed(body.decode("utf-8", errors="ignore"))
        text = " ".join(parser._text).strip()
        pages.append(PageEvidence(url, parser.title, parser.headings, text[:20000]))
        for href, _title in parser.links:
            nxt = _normalize(href, url)
            if nxt and _same_origin(nxt, origin) and nxt not in seen and len(queue) < max_pages * 3:
                queue.append(nxt)
        for raw, alt, hint in parser.assets:
            asset_url = _normalize(raw, url)
            if not asset_url or not _same_origin(asset_url, origin):
                continue
            assets.setdefault(asset_url, OfficialAsset(asset_url, url, _asset_type(asset_url, hint), alt))

    # Promote likely brand assets. Never replace their source; only classify them.
    for asset in assets.values():
        label = f"{asset.url} {asset.alt}".lower()
        if any(k in label for k in ("logo", "wordmark", "brand", "favicon")):
            asset.asset_type = "brand_logo_or_vector"

    claims = []
    for page in pages:
        for heading in page.headings:
            claims.append({
                "claim": heading,
                "source_url": page.url,
                "source_type": "official_website",
                "confidence": "primary_source",
            })

    return {
        "origin": origin,
        "pages": [asdict(p) for p in pages],
        "assets": [asdict(a) for a in assets.values()],
        "claims": claims,
        "policy": {
            "official_origin_only": True,
            "prefer_official_assets": True,
            "never_generate_official_ui": True,
            "never_generate_official_logo": True,
            "source_required_for_product_claims": True,
        },
    }


def save_site_pack(pack: dict, output: str | Path) -> str:
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)

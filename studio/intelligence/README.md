# Official Project Intelligence

PawanStudio does not require a website URL for every project.

## Default behavior

User can simply say:

`Make a video about <project>.`

The discovery/research adapter searches for the project's official identity and candidate first-party sources. Candidates are ranked but **never treated as authoritative until verified**.

If identity confidence is high, the Studio can build/reuse a project knowledge pack automatically. If identity is ambiguous, it asks the user for a seed URL.

A URL supplied by the user remains a preferred seed, not a mandatory requirement.

## Source hierarchy

1. Official website/product pages
2. Official documentation
3. Official GitHub
4. Official blog/announcements
5. Official X/social accounts
6. Primary data
7. Independent sources for context/corroboration

## Asset hierarchy

Official verified logo/UI/announcement/image/video > licensed real media > public-domain media > conceptual generated media.

Generated media must never impersonate an official product interface, logo, announcement, balance, rate, chart or other product-of-record artifact.

## Project memory

The verified source pack and asset vault are reusable per project. Subsequent videos can say only the project name and reuse the approved knowledge/assets. Before production, the pack can be refreshed and changed claims/assets can invalidate only affected scenes where possible.

## Refresh

Recommended default: refresh official sources before each production for time-sensitive projects; otherwise use the cached pack until its configured age expires.

## Required external adapter

`official_discovery.py` is the deterministic core. A browser/search adapter is responsible for live discovery, crawling public pages, extracting assets, following same-site links and verifying official identity. It must write verified `OfficialSource` and `AssetRecord` objects into `ProjectMemory`.

# Official Site Intelligence

PawanStudio can ingest a project's official website once and maintain a cached site-intelligence pack. The pack contains page evidence, headings/claims, discovered first-party images/videos/icons, source URLs and a strict authenticity policy.

## Workflow

1. User enters the project's official URL once.
2. Studio crawls the configured origin and approved paths only.
3. It discovers product pages, blog/docs/FAQ pages and first-party assets.
4. It caches the evidence/asset pack under Studio storage.
5. Creative planning can select official logos, product UI and announcements automatically.
6. Before a time-sensitive production, refresh the pack so changed pages/assets are re-ingested.

## Guarantees

- No cross-domain asset is silently accepted as official.
- Official logo/product proof is preferred over stock or generated media.
- Generated conceptual visuals are never labeled as official product UI.
- Every discovered asset carries its source page and URL for provenance.
- The system is reusable across projects; only the official origin and approved paths change.

For Sats Terminal, configure `https://www.satsterminal.com` and paths such as `/`, `/blog`, `/borrow`, `/borrow/faq`, and `/borrow/learn`.

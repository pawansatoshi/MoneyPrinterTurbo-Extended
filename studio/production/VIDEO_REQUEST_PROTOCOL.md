# PawanStudio Video Request Protocol

This is the mandatory operating contract for every future video request.

## 1. Rules first
Before planning or rendering, load and enforce the current PawanStudio master specification, skill catalog, production pipeline, asset-authenticity policy, creator-identity policy, QC gates, self-healing policy, and project-specific rules. If applicable rules cannot be loaded, BLOCK the job. Never silently fall back to the old slideshow pipeline.

## 2. Project understanding
For each project: resolve official website and first-party sources; inspect official pages, docs, FAQ, blog, announcements, product pages and official social/technical sources when available; build a project brief, terminology map, claims/evidence ledger and official-asset registry; prefer current primary sources; block unsupported/stale claims.

## 2A. STRICT OFFICIAL-ASSET RULE
For branded projects with a publicly accessible official website or first-party product pages, the runtime MUST retrieve/capture required official visual material itself through the configured browser/research/asset adapter BEFORE rendering.

User-uploaded screenshots, screenshots found in chat history, or previously generated project images MUST NOT be silently substituted when an official equivalent is available. They may be used only when the user explicitly requests them, or when they are the user's own creator material rather than project/product material.

Every official product asset in the final timeline MUST have an asset-registry record containing source URL, retrieval timestamp, source type, asset role and provenance status. Final QC MUST verify that each timeline asset matches a registered source asset.

If an official asset is required but cannot be retrieved/verified, production MUST be BLOCKED or use a clearly non-official conceptual treatment. It MUST NOT fabricate an official-looking substitute and MUST NOT silently fall back to a user screenshot.

## 3. Authenticity
Official logo/UI/charts/data/announcements must use verified originals. Conceptual AI visuals are allowed only when clearly conceptual and not presented as official product material. Fabricated official-looking logos, dashboards, balances, rates, product screens or announcements are BLOCKED. Keep provenance metadata.

## 4. Creator identity
If an authorized creator photo/video/voice exists, preserve identity and use the authorized source as the identity anchor. Professional enhancement, framing, cleanup, wardrobe/styling and contextual placement are allowed when supported. Never silently replace the creator with another face or synthetic voice. Choose presenter/photo/voice-over/product-only scenes intelligently; do not paste the creator everywhere.

## 5. Creative direction
Never default to `topic -> stock keywords -> photos -> TTS -> captions -> slideshow`. Generate and score multiple concepts on originality, project relevance, evidence, visual potential, narrative strength, retention, creator fit and platform fit. Identify overused treatments when reference/research adapters permit and deliberately choose a differentiated treatment.

## 6. Production
Normal path: rules -> project discovery -> research -> evidence -> thesis -> story -> differentiation -> visual language -> storyboard -> shot plan -> authentic assets -> creator media -> narration -> captions -> motion -> sound -> edit -> render -> forensic QC -> self-heal -> rerender -> complete QC -> delivery.

The renderer must use purposeful motion, camera language, compositing, diagrams, UI demonstrations, graphics, B-roll and multiple subtitle styles. A still-image slideshow is a QC failure unless explicitly requested by the format.

## 7. Mandatory final inspection
NO video may be delivered merely because rendering succeeds. Final artifact MUST pass all applicable gates: technical integrity; resolution/aspect/FPS/duration; black/frozen-frame checks; available visual anomaly/flicker/warping checks; creator identity/provenance; official product/logo/UI authenticity; claim/evidence verification; narration/pronunciation checks; audio clipping/noise/silence/loudness; subtitle timing/spelling/safe-area/overflow/collision; narration-to-visual correspondence; pacing/dead sections; repetitive-shot/slideshow detection; creative differentiation; asset provenance/licensing metadata; platform requirements.

Missing analysis MUST NOT be treated as PASS. A required gate with no executable analyzer is BLOCKED until the adapter exists or the requirement is explicitly inapplicable.

## 8. Mandatory self-healing
On any failure: identify exact stage/scene/asset/artifact; generate targeted repair plan; apply repair; rerender/reanalyse affected material; run the COMPLETE applicable QC suite again; repeat until PASS or configured safety/retry budget is exhausted. Never deliver a known-failing artifact. If unresolved, final state is BLOCKED with a machine-readable failure report.

## 9. Delivery evidence
A delivered video must include final QC status, detected issues, fixes applied, source/provenance summary, render/version identifier and non-blocking caveats. Never claim checked/rendered/repaired/passed without runtime evidence.

## 10. Project rules
User project constraints override generic defaults. Example: "use only official Sats Terminal assets" is a hard constraint. Merge constraints and fail closed on conflicts.

## 11. No premature delivery
Drafts/previews only when explicitly requested. A normal video request means continue through production and QC until genuinely ready or report a blocking runtime dependency. Never label an unverified draft final.

## 12. Release rule for official screenshots
For any project such as Sats Terminal, the production manifest MUST distinguish `official_source_asset`, `user_creator_asset`, and `conceptual_asset`. The final timeline may contain a product screenshot only if its manifest entry is `official_source_asset` with a verified first-party URL. A file originating from conversation uploads MUST be rejected as a product screenshot unless the user explicitly authorizes that exact file. QC must compare the final media hash/reference against the manifest and fail on mismatch.

## 13. Video-request execution contract
Whenever the user asks to make a video, the runtime MUST execute the complete pipeline and MUST NOT stop after generating a storyboard or draft. It must inspect its own rendered output before delivery. If any issue is found, it must self-heal and repeat the complete QC cycle. Delivery is permitted only after an evidenced PASS.

# PawanStudio Video Request Protocol

This is the mandatory operating contract for every future video request.

## 1. Rules first
Before planning or rendering, load and enforce the current PawanStudio master specification, skill catalog, production pipeline, asset-authenticity policy, creator-identity policy, QC gates, self-healing policy, and project-specific rules. If applicable rules cannot be loaded, BLOCK the job. Never silently fall back to the old slideshow pipeline.

## 2. Project understanding
For each project: resolve official website and first-party sources; inspect official pages, docs, FAQ, blog, announcements, product pages and official social/technical sources when available; build a project brief, terminology map, claims/evidence ledger and official-asset registry; prefer current primary sources; block unsupported/stale claims.

## 2A. STRICT OFFICIAL-ASSET RULE
For branded projects with a publicly accessible official website or first-party product pages, the runtime MUST retrieve/capture required official visual material itself through the configured browser/research/asset adapter BEFORE rendering.

User-uploaded screenshots, screenshots found in chat history, or previously generated project images MUST NOT be silently substituted when an official equivalent is available. They may be used only when the user explicitly requests them, or when they are the user's own creator material rather than project/product material.

Every official product asset in the final timeline MUST have an asset-registry record containing source URL, retrieval timestamp, source type, asset role, provenance status, retrieval method and a cryptographic content hash when technically available. Final QC MUST verify that each timeline asset matches a registered source asset by hash/reference or an equivalent deterministic identity check.

If an official asset is required but cannot be retrieved/verified, production MUST be BLOCKED or use a clearly non-official conceptual treatment. It MUST NOT fabricate an official-looking substitute and MUST NOT silently fall back to a user screenshot.

## 2B. SOURCE/ASSET ISOLATION
Project assets and creator assets MUST be stored in separate namespaces/manifests. Conversation-uploaded project screenshots must be quarantined from automatic project-asset selection. The asset selector MUST reject files classified as `user_project_screenshot`, `chat_screenshot`, `previous_render`, or `unknown_provenance` for branded product/UI scenes unless the user explicitly authorizes that exact file.

Before rendering, run a provenance preflight. Every planned branded asset must be classified as `official_source_asset`, `user_creator_asset`, `conceptual_asset`, or `blocked`. Any unclassified branded asset = BLOCK.

## 2C. OFFICIAL CAPTURE VERIFICATION
A webpage screenshot is not considered official merely because it visually resembles the official site. The runtime MUST retain the source URL and capture metadata and MUST verify that the captured content came from the intended first-party domain. If the browser/research adapter cannot prove source provenance, the capture cannot be used as an official product screenshot.

## 2D. VIEWER-FACING CLEANLINESS
Internal provenance/QC labels such as `OFFICIAL SCREENSHOT`, `OFFICIAL ASSET`, `SOURCE`, `ASSET ID`, internal confidence labels, debug text, file names, hashes and QC markers MUST NEVER appear in the viewer-facing video unless the editorial story explicitly requires that wording. Provenance belongs in manifests/QC reports, not accidental overlays.

## 3. Authenticity
Official logo/UI/charts/data/announcements must use verified originals. Conceptual AI visuals are allowed only when clearly conceptual and not presented as official product material. Fabricated official-looking logos, dashboards, balances, rates, product screens or announcements are BLOCKED. Keep provenance metadata.

Official product material MUST remain visually authentic. Do not redraw, regenerate, hallucinate, or alter product UI in ways that could change meaning. Crop, pan, zoom, highlight and clearly non-semantic presentation effects are allowed.

## 4. Creator identity
If an authorized creator photo/video/voice exists, preserve identity and use the authorized source as the identity anchor. Professional enhancement, framing, cleanup, wardrobe/styling and contextual placement are allowed when supported. Never silently replace the creator with another face or synthetic voice. Choose presenter/photo/voice-over/product-only scenes intelligently; do not paste the creator everywhere.

Creator-photo enhancement MUST preserve identity. If wardrobe transformation is supported, preserve face/identity and use project-appropriate styling. Any generated creator transformation must pass identity-consistency QC before release.

### 4A. CANONICAL CREATOR VOICE REFERENCE
The authorized English creator voice reference is documented at `reference_audio/pawan_english_reference.manifest.json` and the corresponding reference filename is `reference_audio/pawan_english_reference.m4a`.

The reference recording is used ONLY to condition/identify the creator voice. Its spoken sample text must NOT be copied as a finished narration track unless the user explicitly asks for that recording itself. For every new video, generate a fresh project-specific script from current research and render that script through the configured authorized voice workflow.

If the authorized reference audio is not physically available to the runtime, voice-authenticated production is BLOCKED. Do not silently fall back to unrelated generic TTS. A project may use another explicitly approved voice only when its project rules say so.

The reference is creator-controlled material and must not be redistributed outside the configured production environment without explicit authorization.

## 5. Creative direction
Never default to `topic -> stock keywords -> photos -> TTS -> captions -> slideshow`. Generate and score multiple concepts on originality, project relevance, evidence, visual potential, narrative strength, retention, creator fit and platform fit. Identify overused treatments when reference/research adapters permit and deliberately choose a differentiated treatment.

Every storyboard MUST specify why each visual exists and how it advances narration. A scene that merely decorates speech without adding information, emotion, proof or narrative progression should be revised.

## 6. Production
Normal path: rules -> project discovery -> research -> evidence -> thesis -> story -> differentiation -> visual language -> storyboard -> shot plan -> authentic assets -> creator media -> narration -> captions -> motion -> sound -> edit -> render -> forensic QC -> self-heal -> rerender -> complete QC -> delivery.

The renderer must use purposeful motion, camera language, compositing, diagrams, UI demonstrations, graphics, B-roll and multiple subtitle styles. A still-image slideshow is a QC failure unless explicitly requested by the format.

For product/UI scenes, prefer editorial demonstrations: meaningful crops, guided camera movement, pointer/focus, callouts, diagrams, transitions, comparisons and visual explanations. Do not use repeated full-page screenshots as the primary visual language.

## 6A. CREATIVE VARIETY / ANTI-SLIDESHOW GATE
The final timeline MUST be analysed for repetitive stills, repeated full-page screenshots, near-identical frames, excessive hold durations, identical transitions and low visual change. If the video is materially a screenshot/photo slideshow, FAIL the creative gate.

Maintain visual-role diversity where appropriate: presenter, official UI, diagram, data visualization, motion graphic, contextual B-roll, conceptual metaphor, typography and evidence card. Do not force every role into every video.

## 6B. SUBTITLE QUALITY
Subtitles MUST be an editorial layer, not raw transcript text. Select a suitable style from the subtitle catalog, keep text within safe areas, avoid UI collisions, avoid giant distracting text, synchronize to speech, and verify spelling/segmentation. Word highlighting, phrase emphasis, kinetic typography and restrained dynamic treatments may be used when they improve comprehension.

Internal/debug labels are prohibited from subtitle output.

## 6C. AUDIO/VOICE GATE
If the user has supplied an authorized voice sample and requests it, use the authorized voice workflow when available. Do not silently substitute a robotic or unrelated TTS voice. If no authorized voice is available, narration may be omitted or a clearly disclosed project-approved synthetic voice may be used only when project rules permit it.

Audio QC must check silence, clipping, excessive noise, abrupt cuts, loudness consistency, music/narration balance, intelligibility and pronunciation using executable analyzers. Missing required audio analysis = BLOCK unless explicitly inapplicable.

## 7. Mandatory final inspection
NO video may be delivered merely because rendering succeeds. Final artifact MUST pass all applicable gates: technical integrity; resolution/aspect/FPS/duration; black/frozen-frame checks; available visual anomaly/flicker/warping checks; creator identity/provenance; official product/logo/UI authenticity; claim/evidence verification; narration/pronunciation checks; audio clipping/noise/silence/loudness; subtitle timing/spelling/safe-area/overflow/collision; narration-to-visual correspondence; pacing/dead sections; repetitive-shot/slideshow detection; creative differentiation; asset provenance/licensing metadata; platform requirements.

### 7A. BLACK/FROZEN FRAME POLICY
The forensic analyzer MUST detect black frames, near-black intervals, frozen frames and abnormal stillness. Intentional cinematic black may be allowed only when explicitly represented in the storyboard/timeline as an intentional transition or dramatic beat and within configured thresholds. Unplanned black gaps or freezes are FAIL conditions.

### 7B. CLAIM/EVIDENCE POLICY
Every material factual claim must map to a source in the claims/evidence ledger. Time-sensitive claims must have current-source verification. Financial rates, liquidity, APY, balances, launch dates, availability and similar volatile facts MUST carry retrieval timestamps and MUST NOT be presented as current if stale. Unsupported claims = BLOCK.

### 7C. FINAL TIMELINE PROVENANCE POLICY
QC must inspect the actual rendered timeline and map each branded/project visual back to the asset manifest. If any project screenshot is not registered as `official_source_asset` with a verified first-party source, the official-asset gate FAILS. Visual similarity is insufficient.

### 7D. VIEWER-FACING DEBUG/PROVENANCE SCAN
The final rendered frames MUST be scanned for accidental internal labels including `OFFICIAL SCREENSHOT`, `OFFICIAL ASSET`, `SOURCE`, `ASSET ID`, debug strings, file paths and hashes. Any such label outside an intentionally editorial context = FAIL and must be removed before release.

### 7E. BLACK-BAR / FRAMING POLICY
For a requested 16:9 output, the final composition MUST use the full intended frame. Unintentional letterboxing/pillarboxing, oversized empty margins, vertically oriented source media placed as a tiny card, or creator/product content trapped in an unprofessional center box = FAIL. Intentional cinematic bars are allowed only when specified by the visual language and consistently applied.

### 7F. BRAND PROMINENCE POLICY
The project being explained is the primary visual brand. PawanStudio branding is secondary and must not compete with the project. Internal studio names, debug marks or production labels must not be used as prominent viewer-facing overlays unless the creative brief explicitly calls for them.

## 8. Mandatory self-healing
On any failure: identify exact stage/scene/asset/artifact; generate targeted repair plan; apply repair; rerender/reanalyse affected material; run the COMPLETE applicable QC suite again; repeat until PASS or configured safety/retry budget is exhausted. Never deliver a known-failing artifact. If unresolved, final state is BLOCKED with a machine-readable failure report.

Self-healing MUST be targeted but the release decision MUST always be based on a fresh complete QC cycle after each repair. Fixing one black frame does not permit skipping provenance, subtitles, audio, creative or claim checks.

## 8A. PRE-DELIVERY RELEASE CANDIDATE LOOP
The runtime must maintain explicit states: `PLANNED -> RENDERED -> QC_FAILED -> HEALING -> RERENDERED -> QC_RECHECK -> PASS` or `BLOCKED`. PASS is impossible without evidence from the final rendered artifact. A prior draft's QC result cannot be reused for a changed render.

## 8B. NO FALSE PASS / EVIDENCE COMPLETENESS
A QC report is invalid if it says PASS while any mandatory gate is missing, manually asserted, inferred, or based on a previous render. The report must include artifact hash/version, test results, failures, repairs and the exact render tested. If an analyzer is unavailable, the corresponding mandatory gate is BLOCKED, not PASS.

## 9. Delivery evidence
A delivered video must include final QC status, detected issues, fixes applied, source/provenance summary, render/version identifier and non-blocking caveats. Never claim checked/rendered/repaired/passed without runtime evidence.

## 10. Project rules
User project constraints override generic defaults. Example: `use only official Sats Terminal assets` is a hard constraint. Merge constraints and fail closed on conflicts.

## 11. No premature delivery
Drafts/previews only when explicitly requested. A normal video request means continue through production and QC until genuinely ready or report a blocking runtime dependency. Never label an unverified draft final.

## 12. Release rule for official screenshots
For any project such as Sats Terminal, the production manifest MUST distinguish `official_source_asset`, `user_creator_asset`, and `conceptual_asset`. The final timeline may contain a product screenshot only if its manifest entry is `official_source_asset` with a verified first-party URL. A file originating from conversation uploads MUST be rejected as a product screenshot unless the user explicitly authorizes that exact file. QC must compare the final media hash/reference against the manifest and fail on mismatch.

## 13. Video-request execution contract
Whenever the user asks to make a video, the runtime MUST execute the complete pipeline and MUST NOT stop after generating a storyboard or draft. It must inspect its own rendered output before delivery. If any issue is found, it must self-heal and repeat the complete QC cycle. Delivery is permitted only after an evidenced PASS.

## 14. NEVER-CERTIFY-WITHOUT-EVIDENCE
The assistant/runtime MUST NOT claim that a video was checked, rendered, repaired, source-verified, or passed QC unless the corresponding runtime evidence exists for that exact render/version. If evidence is unavailable, report `BLOCKED` rather than infer success from configuration or prior runs.

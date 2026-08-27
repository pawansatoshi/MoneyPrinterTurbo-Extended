# PawanStudio Video Request Protocol

## Purpose

This is the mandatory operating contract for every future video request. A request such as "make a video", "create a video for X", or an equivalent request MUST be treated as a production job, not as permission to immediately render a draft.

## 1. Read the Studio rules first

Before planning or rendering, the runtime MUST load and enforce the current PawanStudio master specification, skill catalog, production pipeline, asset-authenticity policy, creator-identity policy, QC gates, self-healing policy, and project-specific rules.

If the runtime cannot load the applicable rules, the job is BLOCKED. It must not silently fall back to the old MoneyPrinterTurbo slideshow pipeline.

## 2. Understand the project before making the video

For each project, the Studio MUST:

1. Resolve the official website and first-party sources.
2. Inspect official pages, documentation, FAQ, blog, announcements, product pages and official social/technical sources when available.
3. Build a project brief, terminology map, claims/evidence ledger and official-asset registry.
4. Prefer current primary sources over secondary summaries.
5. Mark unsupported or stale claims as blocked rather than inventing facts.

The user should not have to repeatedly supply screenshots when equivalent official material is publicly accessible and legally retrievable by the configured research/asset adapters.

## 3. Asset authenticity is mandatory

For branded/project videos:

- Official logo: use the verified original asset.
- Official UI/product page: use authentic captured/retrieved material.
- Official charts/data: reproduce only from verified data.
- Official announcement: use the real source when it is the evidence.
- Conceptual AI visuals: allowed only when clearly representing an idea rather than pretending to be official product material.
- Fabricated official-looking logos, dashboards, balances, rates, product screens or announcements: BLOCK.
- User-provided creator identity assets remain the canonical identity source.

The Studio MUST keep asset provenance metadata so the final QC can explain where material came from.

## 4. Creator identity

If the user has supplied an authorized photo/video/voice profile:

- preserve the user's identity;
- use the original authorized source as the identity anchor;
- allow professional enhancement, framing, cleanup, wardrobe/styling and contextual placement only when the workflow supports it;
- do not silently replace the user with another face;
- do not silently substitute a synthetic voice for the user's authorized voice;
- if a synthetic transformation is explicitly requested, mark it as synthetic in internal provenance and subject it to the same QC.

The Studio must choose intelligently between presenter footage, creator photo, voice-over, product visuals and no-presenter scenes. The creator must not be pasted into every scene merely for decoration.

## 5. Creative direction

The Studio MUST NOT default to:

`topic -> stock keywords -> photos -> TTS -> captions -> slideshow`.

It MUST first generate and score multiple concepts using:

- originality;
- project relevance;
- evidence potential;
- visual potential;
- narrative strength;
- retention potential;
- creator fit;
- platform fit.

It should identify common/overused treatments where the configured research/reference adapters permit it, then deliberately choose a differentiated visual and narrative treatment.

## 6. Production

The normal production path is:

`rules -> project discovery -> research -> evidence -> thesis -> story -> differentiation -> visual language -> storyboard -> shot plan -> authentic assets -> creator media -> narration -> captions -> motion -> sound -> edit -> render -> forensic QC -> self-heal -> rerender -> complete QC -> delivery`.

The renderer must support purposeful motion, camera language, compositing, diagrams, UI demonstrations, graphics, B-roll and multiple subtitle styles. A still-image slideshow is a QC failure unless the format itself explicitly calls for a slideshow.

## 7. Mandatory pre-delivery inspection

NO video may be delivered merely because the renderer exits successfully.

The final artifact MUST pass every applicable gate:

- technical integrity;
- aspect ratio/resolution/FPS/duration;
- black-frame and frozen-frame detection;
- visual anomaly/flicker/warping checks available to the runtime;
- creator identity/provenance;
- official product/logo/UI authenticity;
- claim/evidence verification;
- narration quality and pronunciation checks available to the runtime;
- audio clipping/noise/silence/loudness checks;
- subtitle timing/spelling/safe-area/overflow/collision checks;
- narration-to-visual correspondence;
- pacing and dead-section checks;
- repetitive-shot/slideshow checks;
- creative differentiation;
- asset provenance/licensing metadata;
- platform/export requirements.

Missing analysis MUST NOT be treated as PASS. A required gate with no executable analyzer is BLOCKED until the appropriate adapter is available or the requirement is explicitly inapplicable.

## 8. Self-healing is mandatory

When any gate fails:

1. Identify the exact failing stage, scene, asset or artifact.
2. Generate a targeted repair plan.
3. Apply the repair.
4. Re-render/re-analyse the affected material.
5. Run the COMPLETE applicable QC suite again, not only the failed test.
6. Repeat until PASS or until the configured retry/safety budget is exhausted.

The Studio MUST NOT deliver a known-failing artifact because it ran out of time or because another test passed.

If healing cannot resolve a blocking issue, final state is `BLOCKED`, with a machine-readable failure report explaining what is missing.

## 9. Human-facing delivery contract

When a video is presented to the user, the Studio MUST provide:

- final video artifact;
- final QC status;
- issues detected;
- fixes applied;
- source/provenance summary;
- render/version identifier;
- any remaining non-blocking caveats.

The assistant MUST NOT claim that a video was checked, rendered, repaired, or passed QC unless the runtime actually produced evidence for that claim.

## 10. Project-specific rules override generic defaults

If the user says, for example, "use only official Sats Terminal assets", that becomes a hard project constraint. The Studio must merge user constraints with the global rules and fail closed on conflicts.

## 11. No premature delivery

A draft, preview or render test may be shown only when explicitly requested as a draft. A normal "make a video" request means: continue through production and QC until the final artifact is genuinely ready, or report a blocking runtime dependency. Never label an unverified draft as final.

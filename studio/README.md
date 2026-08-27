# Pawan Video Studio

Pawan Video Studio is the reusable creative-production layer above MoneyPrinterTurbo. Projects change; the production system stays.

## What is now covered

### Creative directors

- Cinematic
- Product Demo
- Tech Explainer
- Documentary
- Launch / Hype
- News
- Talking Head
- Podcast
- Motion Graphics
- Gaming / High Energy
- Shorts / Reels
- Localization

Directors can be mixed. A project can use `product_demo + cinematic + shorts` without changing renderer code.

### Visual language

The Studio distinguishes four layers:

1. **Product proof** — authentic screenshots, recordings and official logos.
2. **Conceptual B-roll** — licensed/public-domain footage or clearly conceptual AI visuals.
3. **Editorial typography** — hooks, statistics, quotes and CTAs.
4. **Narration captions** — accessible speech captions, independently styled and timed.

A product claim must not be represented by fabricated UI.

### Camera / editing vocabulary

Push, pull, pan, drift, parallax, macro UI push, subject follow, UI-region follow, simulated rack focus, beat zoom, whip transitions, match cuts, mask reveals, speed ramps, J/L cuts, punch-ins, freeze frames, montages and loop endings are part of the reusable vocabulary.

### Product UI engine

Product assets can be treated as semantic objects with regions such as `headline`, `borrow_amount`, `collateral`, `ltv`, `rate`, `cta`, `chart`, and `loan_health`. The creative planner can direct the camera to a region instead of moving a screenshot randomly.

### Subtitle engine

Subtitle timing supports sentence, phrase, word, karaoke, character and automatic selection. Visual families include clean, premium/minimal, word-pop, phrase-pop, kinetic, bounce, typewriter, highlight, outline, shadow, lower-third, speaker label, dual-language, emphasis, social-bold, news, technical and comic. These are composable with animation, anchor, safe-area and emphasis rules.

### Voice engine

`studio/voice/providers.json` defines a provider-neutral interface with Chatterbox as the preferred local expressive provider, Kokoro as a fast local alternative and Piper as a lightweight fallback. Voice cloning requires consent and provenance. The repository does not embed third-party model weights.

### Media and provenance

`studio/media/sources.json` defines adapters for Pexels, Pixabay, Wikimedia, Internet Archive, NASA and AI-generated conceptual media. Each external asset should retain source URL, retrieval date, license, commercial-use status, attribution and provenance.

### Audio

The production model includes natural voice, pacing, pauses, emphasis, pronunciation dictionaries, music beds, voice ducking, UI clicks, whooshes, impacts, risers, ambience, room tone, silence cleanup and loudness normalization.

### Structured production plan

`production.schema.json` is the contract between the creative planner and renderer. A scene can specify asset, camera, transition, motion graphics, callouts and caption mode. This makes the system deterministic, editable and reusable.

### Quality director

`qc/rules.json` defines technical, visual, audio, story, trust and accessibility checks. Trust checks include official-asset validation, source-claim validation, license provenance and launch-date verification. A failed trust check should block the master.

## Project model

A project supplies a manifest, assets, narration/audio and optional word-level transcript. The Studio should never require project-specific renderer code.

## Example

```bash
python -m studio.render project.json --output storage/studio/final.mp4
```

## Roadmap

The architecture is in place for the next implementation layers: provider adapters, semantic UI-region detection, free-media retrieval, AI B-roll adapters, motion-graphics rendering, automatic story/shot planning, full QC execution and multi-format reframe rendering. These integrations remain optional so the core Studio continues to run without external paid services or model weights.

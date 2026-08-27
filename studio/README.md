# Pawan Video Studio

Pawan Video Studio is the reusable creative-production layer above MoneyPrinterTurbo. Projects change; the production system stays.

## Implemented production system

### Creative directors
Cinematic, product demo, tech explainer, documentary, launch/hype, news, talking head, podcast, motion graphics, gaming/high-energy, Shorts/Reels and localization. Directors are composable and project-independent.

### Visual language
The Studio separates product proof, conceptual B-roll, editorial typography and narration captions. Authentic project screenshots, recordings and official logos are preferred for product claims; fabricated product UI is prohibited.

### Camera / editing vocabulary
Push/pull, pans, drift, parallax intent, macro/UI focus intent, subject-follow intent, beat zoom intent, match cuts, whip cuts, crossfades, punch-ins, freeze frames, montage, J/L-cut concepts, pattern breaks and loop endings are represented in the production model. The planner normalizes executable camera primitives while retaining semantic camera intent.

### Product UI
Scenes can carry semantic UI-region intent such as headline, amount, collateral, LTV, rate, chart, health and CTA. Product screenshots remain source assets rather than being regenerated as fake UI.

### Subtitles
Sentence, phrase, word, karaoke, character and automatic timing are supported. The preset registry includes clean/premium, word-pop, phrase-pop, kinetic, bounce, typewriter, highlight, outline, shadow, lower-third, speaker label, dual-language, emphasis, minimal, social-bold, news, technical and comic families. Safe-area and two-line constraints are enforced by the renderer.

### Voice
`studio/voice/providers.json` is provider-neutral. Chatterbox is the preferred expressive local provider, Kokoro is a fast local alternative, and Piper is a lightweight fallback. `studio/voice/runtime.py` provides the executable adapter contract and writes voice provenance metadata. Provider/model installation remains environment-specific; model weights are intentionally not committed to Git.

### Media
`studio/media/sources.json` defines official-first, user asset, licensed stock, public-domain/archive, NASA/Wikimedia and AI-conceptual source classes with per-asset provenance requirements.

### Audio
The production model supports natural narration, pacing, pauses, emphasis, pronunciation dictionaries, music beds, voice ducking, UI clicks, whooshes, impacts, risers, ambience, room tone, silence cleanup and loudness normalization.

### Structured production plan
`production.schema.json` is the contract between planning and rendering. `studio/pipeline.py` now orchestrates preflight → creative plan → render → technical QC.

### Quality gate
`studio/qc/preflight.py` blocks invalid manifests before rendering. `studio/qc/check.py` validates the rendered master for video/audio streams, duration, dimensions/aspect ratio and FPS. The existing rules registry remains the source for additional visual, audio, trust and accessibility checks.

## Commands

Preflight:

```bash
python -m studio.qc.preflight studio/project.template.json
```

Render + technical QC:

```bash
python -m studio.pipeline studio/project.template.json --output storage/studio/final.mp4
```

Direct renderer:

```bash
python -m studio.render studio/project.template.json --output storage/studio/final.mp4
```

TTS adapter:

```bash
python -m studio.voice.runtime chatterbox narration.txt assets/audio/narration.wav
```

## Output formats

Projects are format-aware: **16:9**, **9:16** and **1:1**. The standard YouTube/master template is **1920×1080, 30 FPS**. Reels/Shorts and square variants are selected through the project manifest rather than changing renderer code.

## Important boundary

The Studio is now the reusable production architecture, but external capabilities are intentionally adapters: TTS models, stock APIs, AI-video/image models and advanced computer-vision detectors must be installed or configured in the execution environment. The repository does not pretend those third-party runtimes are present when they are not.

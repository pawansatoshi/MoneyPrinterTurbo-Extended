# Pawan Video Studio

## What this repository is becoming

`pawansatoshi/MoneyPrinterTurbo-Extended` is the permanent codebase for our own reusable video-production studio. The **project changes; the studio does not**.

We use the existing MoneyPrinterTurbo/Extended pipeline for script, footage, TTS and task orchestration, then build our own premium Studio layer for the part that matters most visually: composition, dynamic subtitles, camera movement, product UI treatment, brand profiles and repeatable creative direction.

## Core contract

### Project-specific
- logo
- official website
- official product screenshots/screen recordings
- approved B-roll
- narration/script
- disclaimer
- brand colors/fonts
- CTA
- launch-date facts

### Studio-wide
- subtitle engine
- word highlighting
- camera language
- scene transitions
- safe areas
- crop/cover behavior
- cinematic motion
- output profiles
- render quality
- reusable templates

This separation prevents Sats Terminal logic from leaking into the next project.

## Dynamic subtitle system

The studio never uses the old “giant text across the screen” approach.

Default behavior:
- maximum 2 lines;
- measured text wrapping;
- rounded translucent caption card;
- bottom safe area;
- high contrast;
- optional word-by-word highlight driven by the Extended subtitle JSON;
- project accent color controls the active word;
- subtitle size is independent from video resolution.

## Dynamic camera system

Every scene can specify a camera move or `auto`:

`push_in` · `pull_out` · `pan_left` · `pan_right` · `pan_up` · `pan_down` · `drift_left` · `drift_right` · `drift_up` · `drift_down` · `center` · `auto`

`auto` is seeded, so the same project can be reproduced exactly. Change the seed to create a fresh cut without changing the creative brief.

## Authentic-product rule

For product campaigns, official UI is evidence. The Studio can animate, crop and move a supplied screenshot, but it must not invent a dashboard, rate, balance, APY, LTV, partner logo or product state.

AI-generated footage belongs in the conceptual/B-roll layer unless the project owner explicitly marks it as product-authentic.

## Current Sats Terminal project

A starter manifest exists at:

`studio/projects/sats-terminal.json`

It references the official product screenshots supplied for the current campaign. The actual binary assets stay project-local and are not fabricated by the engine.

## Rendering

CLI:

```bash
python -m studio.render studio/projects/sats-terminal.json --output storage/studio/sats-terminal.mp4
```

API:

- `GET /api/v1/studio/cameras`
- `POST /api/v1/studio/render`
- `GET /api/v1/studio/tasks/{task_id}`

## Roadmap

1. **Studio Engine v1** — dynamic camera + safe subtitles + project manifests. **Implemented.**
2. **Studio UI** — project picker, scene cards, camera selector, subtitle controls and live preview.
3. **Brand system** — reusable brand profiles and asset libraries.
4. **Cinematic B-roll** — optional AI/video providers with explicit source labels.
5. **Timeline intelligence** — automatic beat/scene timing from narration.
6. **Creator templates** — launch, explainer, product demo, documentary, comparison and announcement.
7. **Quality gate** — automatically flag fake-looking product UI, subtitle overflow and unsupported factual claims.

The goal is not to make another generic AI video generator. The goal is to make **our production studio**.

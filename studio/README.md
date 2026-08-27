# Pawan Video Studio

This repository is no longer treated as a one-off MoneyPrinterTurbo fork. The `studio/` layer is the reusable production system: projects change, the rendering engine stays.

## Design principles

- **Project-agnostic:** Sats Terminal, YeBlock, XREIGN, or a future project are data/config only.
- **Authentic product UI first:** official screenshots, screen recordings and logos are treated as source assets. The engine never fabricates a product dashboard.
- **Dynamic subtitles:** safe-area, maximum two lines, compact rounded caption cards, and optional word-timing data from the existing enhanced subtitle pipeline.
- **Dynamic camera:** every scene can use `push_in`, `pull_out`, `pan_left`, `pan_right`, `pan_up`, `pan_down`, `drift_*`, `center`, or `auto`.
- **Deterministic randomness:** `seed` lets us reproduce a cut; changing the seed generates a different camera sequence without changing the project.
- **Format-aware:** 9:16, 16:9 and 1:1 are controlled by the manifest rather than hard-coded edits.
- **Cinematic but restrained:** motion is deliberately subtle; product UI should remain readable.

## Project model

A project should provide only:

1. `project.json` — brand profile, output format and scene plan.
2. `assets/` — official product media plus approved conceptual footage.
3. `audio.mp3` — final narration.
4. `subtitle.srt` — normal captions.
5. `subtitle_enhanced.json` — optional word-level timing from the existing Extended subtitle system.

The renderer is reusable for every project.

## Camera language

| Mode | Use |
|---|---|
| `push_in` | product reveal / important UI |
| `pull_out` | conclusion / context |
| `pan_left/right` | wide screenshot or dashboard |
| `pan_up/down` | tall mobile UI |
| `drift_*` | cinematic B-roll |
| `auto` | deterministic random choice from the safe set |
| `center` | critical UI that must not move |

## Subtitle rules

Never render a giant full-screen sentence. The studio automatically:

- limits text to two lines;
- wraps by actual rendered width;
- keeps a bottom safe margin;
- uses a compact rounded translucent card;
- keeps the caption readable over bright UI;
- can consume the repository's enhanced word-timing JSON.

## Example

```bash
python -m studio.render project.json --output storage/studio/final.mp4
```

The Studio layer is intentionally additive: the original MoneyPrinterTurbo API and pipeline remain available while this renderer is developed as the premium production path.

# Pawan Video Studio — Subtitle Skills

The Studio treats subtitles as a first-class editorial system, not a single caption style. A project can select a preset per scene or let the Creative Director choose automatically.

## Core subtitle families

1. **clean** — restrained two-line captions, safe-area placement, ideal for documentaries and product films.
2. **word_pop** — one spoken word changes emphasis at a time.
3. **karaoke** — word-level progress/highlight follows speech timing.
4. **phrase_pop** — short phrases enter/exit as semantic beats.
5. **kinetic** — words/phrases animate with scale/position for high-energy videos.
6. **bounce** — controlled elastic entrance for Shorts and entertainment.
7. **typewriter** — characters reveal progressively; use sparingly for intros or storytelling.
8. **highlight_box** — active word/phrase receives a compact highlight chip.
9. **outline** — high-contrast outlined text for busy footage.
10. **shadow** — clean text with strong readability shadow for cinematic footage.
11. **lower_third** — caption sits in a broadcast-style lower-third region.
12. **speaker_label** — speaker name + caption for interviews/podcasts.
13. **dual_language** — primary and translated line with independent typography.
14. **emphasis** — normal captions with selected keywords promoted to editorial typography.
15. **minimal** — tiny unobtrusive captions for premium brand films.
16. **social_bold** — larger, high-retention captions for Shorts/Reels.
17. **news_broadcast** — compact broadcast caption treatment.
18. **technical** — monospace/label treatment for code, metrics and technical explanations.
19. **comic** — playful pop treatment for entertainment/meme content.
20. **auto** — Creative Director selects based on format, genre, shot density and speech cadence.

## Non-negotiable quality rules

- Never render a full-width opaque caption bar unless the selected style explicitly calls for it.
- Default maximum is two lines.
- Measure rendered text width before placing it.
- Respect title/action-safe margins and avoid product UI controls.
- Never cover a detected important UI region when a free safe region exists.
- Word-level styles require word timestamps; fall back gracefully to phrase/SRT timing.
- Avoid rapid flashing: minimum readable word/phrase duration is configurable.
- Keep subtitle typography separate from editorial on-screen titles and UI callouts.
- Preserve punctuation and natural line breaks; never split a product name or URL awkwardly.
- Provide per-format presets for 16:9, 9:16 and 1:1.
- Provide accessibility options: larger font, high contrast, outline, background opacity and reduced motion.

## Timing modes

- `sentence` — one caption per sentence/phrase.
- `phrase` — semantic chunks selected by punctuation and duration.
- `word` — active word highlight.
- `karaoke` — continuous progress/highlight.
- `character` — typewriter reveal.
- `beat` — captions align to music/edit beats when beat metadata exists.

## Style parameters

Every preset can override:

- font family / weight
- font size
- maximum lines
- maximum width
- position / safe-area anchor
- fill / outline / shadow
- background shape and opacity
- active-word color
- entrance / exit animation
- animation duration
- line spacing
- letter spacing
- capitalization
- punctuation behavior
- reduced-motion behavior

The visual renderer must consume these parameters instead of hard-coding one subtitle appearance.

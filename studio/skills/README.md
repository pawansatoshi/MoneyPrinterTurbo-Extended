# Pawan Video Studio Skills

This directory defines the reusable creative vocabulary of the Studio. A project selects and composes skills; it does not fork the renderer.

## Creative directors

`cinematic`, `product_demo`, `tech_explainer`, `documentary`, `launch_hype`, `news`, `talking_head`, `podcast`, `motion_graphics`, `gaming`, `shorts`, and `localization` are the first-class director profiles in `catalog.json`.

## Composition principle

The Studio separates:

- narration captions
- editorial typography
- product UI callouts
- lower thirds
- statistics / quote cards
- disclaimers

They must never be rendered as one generic subtitle layer.

## Asset decision rule

1. Prefer supplied/official product assets for product claims.
2. Use licensed or public-domain footage for factual context.
3. Use AI-generated visuals only for clearly conceptual material.
4. Keep provenance metadata for every external asset.
5. Never fabricate a product interface, logo, partner, statistic, or announcement.

## Camera rule

Camera movement is selected from the semantic role of a shot. `ui_region_follow`, `macro_push`, `subject_follow`, `parallax`, and `beat_zoom` are intentional alternatives to random Ken-Burns motion.

## Quality rule

Every render should pass technical, visual, audio, caption, factual-claim, and asset-provenance checks before being considered a master.

## Style mixing

Directors are composable. For example:

`product_demo + cinematic + shorts`

means product-proof visuals, cinematic pacing, and short-form retention/editing rules. The system must describe style attributes rather than imitate a living creator's exact voice or signature content.

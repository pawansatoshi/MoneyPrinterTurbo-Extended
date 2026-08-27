# PawanStudio Master Build Specification

PawanStudio is a reusable, project-independent AI-assisted production studio built above MoneyPrinterTurbo. It must turn a natural-language brief into an evidence-driven, creator-quality video while preserving authentic product assets and existing rendering infrastructure.

## Product contract

Input can be conversational: project, audience, goal, references, constraints, desired platform and style. The Studio should infer missing production decisions, expose them for review, and preserve approved decisions in project memory.

Pipeline:

Conversation -> Project Memory -> Research -> Claim/Evidence Graph -> Thesis -> Story -> Visual Language -> Storyboard -> Shot Plan -> Asset Intelligence -> Voice -> Captions -> Motion Graphics -> Music/SFX -> Timeline -> Render -> Director Critique -> Targeted Revision -> QC -> Platform Masters.

## Master Director

The Master Director owns the final creative decision and delegates to specialist skills. Specialists are workers, not competing autonomous directors.

Required workers:
- research
- fact checking
- story/thesis
- hook/re-hook/retention
- visual metaphor
- shot design
- product/UI demo
- talking head
- documentary
- cinematic
- tech explainer
- launch/hype
- news
- motion graphics
- B-roll
- asset/provenance
- typography/subtitles
- voice
- music/SFX
- thumbnail/title
- localization
- platform adaptation
- quality/revision

## Research and evidence

Every factual claim must have source metadata. Prefer official website/docs/GitHub/announcements and primary data, then independent sources. Unsupported claims are blocked from factual narration. Product claims require authentic official assets whenever available. Launch dates and time-sensitive facts must be re-verified before export.

Claim record fields: claim, source, source_type, URL/reference, retrieved_at, publication_date, confidence, supporting_evidence, visual_proof, status.

## Authentic asset policy

Asset priority:
1. official logo/product UI/announcement
2. licensed real footage/images
3. public-domain/approved archives
4. generated conceptual media

Never fabricate an official website, logo, dashboard, chart, announcement or person. Generated media must be marked as conceptual where appropriate. Store provenance/license metadata for every external asset.

## Visual language

The Studio must mix visual primitives rather than produce screenshot slideshows:
- authentic UI/screen recordings
- talking head
- stock/public-domain B-roll
- conceptual AI B-roll
- diagrams
- charts
- maps
- timelines
- kinetic typography
- UI callouts
- phone/browser/device mockups
- transitions
- particles/abstract atmosphere

Visual metaphor engine maps abstract concepts to explainable visuals. Product proof always outranks decorative B-roll when a real product view exists.

## Shot director

Each shot is structured data containing timing, purpose, narration, visual source, camera primitive/intent, transition, caption mode, motion graphics, SFX, music cue, provenance and QC expectations. Camera should follow meaningful UI regions or subjects when possible, not apply random zooms.

## Creator-presenter system

Users may provide their own photos and voice samples. A consent-aware Creator Profile stores supplied identity/voice references, preferred framing, delivery characteristics and presentation rules. Use only the user's own/authorized likeness and voice. Do not clone or imitate third-party creators without permission.

Presenter decisions: hook, opinion, explanation and CTA may use the creator; abstract concepts and product proof should switch to B-roll/UI/graphics. Do not promise deception or indistinguishability; optimize for natural, faithful presentation.

## Voice system

Provider abstraction must support local/open models such as Chatterbox, Kokoro and Piper, with optional external providers. Voice controls: pace, emotion, energy, pauses, emphasis, pronunciation and consistency. Generate word/phrase timestamps for captions. Keep model weights outside the repository and make providers optional. Validate voice consent/ownership metadata.

## Subtitle and typography system

Subtitle is distinct from editorial typography and UI callouts.

Timing modes: sentence, phrase, word, karaoke, character, speaker, beat, auto.

Visual families include: clean, premium, minimal, social bold, word pop, active-word, phrase pop, karaoke, typewriter, bounce, slide, fade, outline, shadow, highlight box, kinetic, statistic, quote, hook, CTA, warning, lower third, speaker label, dual-language, documentary, news, technical/code, meme, cinematic, masked reveal, glitch, elastic, blur, wipe, tracking, stretch, shake and object/speaker-follow.

Layout must be safe-area aware, face-aware and UI-aware. Prevent caption collisions and never cover important product controls. Allow composable timing + layout + animation + emphasis rather than a fixed list of styles.

## Editing and retention

Use pattern breaks intentionally. Re-hooks must introduce a new question, evidence or revelation; never use empty clickbait. Scene retention checks should score curiosity, information density, visual change, emotional movement, unresolved question and payoff. Long low-information shots are sent back for revision.

## Audio

Separate narration, music, ambience and SFX. Apply loudness normalization, peak checks, ducking, clean transitions and silence detection. SFX should support editorial beats rather than overwhelm narration.

## Motion graphics

Provide reusable primitives: arrows, pointers, circles, underlines, labels, badges, counters, charts, diagrams, timelines, masks, highlights and kinetic text. Animations: pop, draw-on, slide, wipe, reveal, scale, bounce, type-on, blur, elastic, glitch and beat-synced emphasis.

## Platform adaptation

One story may produce separate narrative cuts for YouTube 16:9, Shorts 9:16, X, Instagram Reels and LinkedIn. Do not merely crop. Reframe subjects/UI and shorten/restructure narrative according to platform intent. Preserve factual claims and provenance across derivatives.

## Packaging

Thumbnail Director produces multiple concepts with focal point, emotion, curiosity and 3-5 word maximum text. Title Laboratory generates curiosity, contrarian, educational, news, story and search-oriented variants, scoring clarity, specificity, credibility and promise consistency.

## Quality Director

Before release, inspect: black bars, framing, unreadable UI, caption collisions, text overflow, duplicate shots, frozen frames, transition errors, audio clipping, loudness, silence, voice/music balance, caption sync, factual citations, official-asset authenticity, license provenance, launch-date freshness, CTA, pacing and story payoff.

If failed, identify the responsible module, revise only the affected plan/scenes, re-render and run QC again. A master cannot be marked ready solely because FFmpeg completed successfully.

## Model/provider strategy

No single model is mandatory. Use adapter interfaces for reasoning, research, voice, image generation and video generation. Open/local tools should be first-class; external providers are optional accelerators. Keep secrets out of git and provide environment-variable configuration.

## Implementation rule

Do not create mock features that claim to be implemented. Every capability must have: schema/API, executable implementation or explicit adapter boundary, tests/acceptance checks, and a documented fallback. Preserve MoneyPrinterTurbo's existing renderer, TTS, subtitle and WebUI capabilities rather than replacing working infrastructure.

## Definition of done

A Studio release is complete only when a real project can travel through the end-to-end path from conversational brief to researched story, evidence-backed shot plan, authentic/attributed assets, natural authorized voice, dynamic captions, motion/audio design, platform masters and automated director QC with targeted revision. Architecture-only registries do not count as production-complete.

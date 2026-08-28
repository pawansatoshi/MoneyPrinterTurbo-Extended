# PawanStudio Creator Voice Reference

This directory stores authorized creator reference audio used for voice cloning/reference conditioning.

## Canonical creator voice

- **Profile:** Pawan Upadhyay — English creator voice
- **Reference filename:** `pawan_english_reference.m4a`
- **Source:** user-supplied recording in the ChatGPT production session
- **Purpose:** voice-reference only; the sample's spoken script is NOT automatically reused as video narration
- **Use:** future scripts are generated per project, then rendered using the authorized creator voice when the local TTS/voice-cloning runtime is available
- **Substitution rule:** never silently replace the creator voice with an unrelated synthetic voice

## Required behavior

1. Treat the creator reference as an identity/reference asset, not as a finished narration track.
2. Generate a fresh project-specific script from research and the project's creative brief.
3. Synthesize/render the new script using the authorized creator voice only when the configured voice engine is available.
4. Match pacing, emphasis and pauses to the scene edit.
5. Run audio QC and voice-provenance checks before delivery.
6. If the reference audio is unavailable to the runtime, the video is BLOCKED rather than silently using generic TTS.

## Supported formats

`.wav`, `.mp3`, `.flac`, `.m4a`

## Reference quality

Preferred reference: 10–60 seconds of clean, single-speaker natural speech with minimal background noise. The supplied English sample is approximately 20 seconds and is suitable as a reference candidate.

## Privacy / repository rule

Reference audio is creator-controlled material. Do not publish or redistribute it outside the configured private/local production environment unless explicitly authorized by the creator. A repository checkout must not assume that a reference file is public merely because its metadata is documented here.

## Important

The reference recording is **not** the final narration for any particular video. PawanStudio must create project-specific narration from the current script and then apply the authorized voice reference.

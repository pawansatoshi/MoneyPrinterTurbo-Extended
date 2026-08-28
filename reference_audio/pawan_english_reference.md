# Pawan English Voice Reference

Status: AUTHORISED CREATOR VOICE REFERENCE
Language: English
Purpose: Voice cloning/reference only. The sample recording itself must NOT be inserted verbatim into future videos unless explicitly requested.

Source file supplied by creator in ChatGPT conversation: `My recording 1.mp3`
Duration: approximately 20.317 seconds
Channels: mono
Sample rate: 44.1 kHz
SHA-256 of supplied source: `1f4e74f8438f580dac1451c62c7a8022b11fdb667006081132ef78a1dff89c81`

## Future-use rule

When the creator requests an English video, this reference should be selected as the preferred authorised creator voice reference for the English narration pipeline, when the actual reference file is available to the runtime.

The runtime must generate a NEW project-specific script from current project research. It must not reuse the sample's spoken sentences merely because this reference exists.

The runtime must preserve the creator's identity and must not substitute an unrelated voice. If this reference file is unavailable to the rendering/voice runtime, the video must be BLOCKED rather than silently using a robotic/unrelated voice when creator voice is required.

## Privacy / provenance

This is a creator-provided private voice reference. Do not publish, redistribute, expose, or use it for unrelated speakers or projects. Keep it separate from project/product assets. Product videos must never treat this voice reference as an official project asset.

## Important technical limitation

The GitHub contents connector used for repository editing cannot upload arbitrary binary audio bytes. Therefore this text manifest records the exact supplied reference and its hash, but it is NOT a replacement for the actual MP3 bytes. The runtime must receive the real audio file through its secure/local asset mechanism before voice cloning can execute.

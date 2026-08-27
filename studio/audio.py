"""Audio policy: adapters for local TTS/voice assets and music/SFX mixing."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

class AudioEngine:
    """Provider-neutral audio adapter. Existing Chatterbox remains the local TTS provider."""
    def __init__(self, tts_provider: str = "chatterbox"):
        self.tts_provider = tts_provider

    def validate_voice_reference(self, path: str) -> bool:
        p=Path(path)
        return p.exists() and p.suffix.lower() in {".wav",".mp3",".m4a",".flac"}

    def build_ffmpeg_mix(self, narration: str, music: str | None = None, sfx: list[str] | None = None) -> list[str]:
        """Return an ffmpeg filter graph; execution is intentionally delegated to the renderer."""
        inputs=[]; filters=[]
        if narration: inputs.append(narration)
        if music: inputs.append(music)
        if sfx: inputs.extend(sfx)
        if not inputs: return []
        if len(inputs)==1: return inputs
        return ["-filter_complex", "amix=inputs=%d:duration=longest:dropout_transition=2" % len(inputs), "-ac", "2"]

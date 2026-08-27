"""Explicit provider registry for footage, AI video, images and TTS.

Providers are opt-in adapters. Unknown providers never silently fabricate assets.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Provider:
    name:str
    kind:str
    requires_key:bool
    source_label:str

PROVIDERS={
 "local":Provider("local","asset",False,"user-supplied"),
 "pexels":Provider("pexels","footage",True,"Pexels"),
 "pixabay":Provider("pixabay","footage",True,"Pixabay"),
 "chatterbox":Provider("chatterbox","tts",False,"Chatterbox local TTS"),
 "ai-video":Provider("ai-video","video",True,"AI-generated conceptual footage"),
}

def get_provider(name:str)->Provider:
    if name not in PROVIDERS: raise ValueError(f"Unsupported provider: {name}")
    return PROVIDERS[name]

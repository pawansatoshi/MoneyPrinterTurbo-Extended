"""Free MIT-licensed creator-voice narration backend using Chatterbox Multilingual."""
from __future__ import annotations
import os
from pathlib import Path
import torch
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

LANG_CODES = {"english": "en", "hindi": "hi", "hinglish": "hi"}

def synthesize(text_path: Path, reference_wav: Path, output_wav: Path, language: str) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    model.prepare_conditionals(str(reference_wav), exaggeration=0.5)
    text = Path(text_path).read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("Narration script is empty")
    code = LANG_CODES.get(language.lower())
    if code is None:
        raise ValueError(f"Unsupported narration language: {language}")
    wav = model.generate(text, language_id=code, audio_prompt_path=str(reference_wav), exaggeration=0.5, cfg_weight=0.4)
    ta.save(str(output_wav), wav.cpu(), model.sr)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("reference_wav")
    p.add_argument("output_wav")
    p.add_argument("language")
    a = p.parse_args()
    synthesize(Path(a.text), Path(a.reference_wav), Path(a.output_wav), a.language)

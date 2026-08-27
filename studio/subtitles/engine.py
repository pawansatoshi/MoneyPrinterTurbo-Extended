"""Composable subtitle renderer primitives for Pawan Video Studio.

This module intentionally separates caption timing, visual treatment, safe-area
placement and animation. It can be used by MoviePy, Remotion or another renderer.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

PRESETS_PATH = Path(__file__).with_name("presets.json")

@dataclass
class Word:
    text: str
    start: float
    end: float
    emphasis: bool = False
    speaker: str | None = None

@dataclass
class CaptionEvent:
    start: float
    end: float
    text: str
    words: list[Word]
    style: str = "clean"
    anchor: str = "bottom_center"
    animation: str = "fade"
    emphasis_words: list[int] | None = None
    speaker: str | None = None


def load_presets(path: str | Path = PRESETS_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_words(words: list[dict[str, Any]]) -> list[Word]:
    result=[]
    for w in words:
        text=str(w.get("text", w.get("word", ""))).strip()
        if not text: continue
        result.append(Word(text=text, start=float(w["start"]), end=float(w["end"]),
                           emphasis=bool(w.get("emphasis", False)), speaker=w.get("speaker")))
    return result


def infer_emphasis(words: list[Word]) -> list[int]:
    """Conservative emphasis heuristic; a future LLM can replace this without changing the schema."""
    out=[]
    for i,w in enumerate(words):
        raw=re.sub(r"[^A-Za-z0-9%$.-]", "", w.text)
        if w.emphasis or raw.isupper() or raw.startswith(("$", "#")) or raw.endswith("%"):
            out.append(i)
    return out


def build_events(transcript: list[dict[str, Any]], style: str = "auto") -> list[CaptionEvent]:
    presets=load_presets()["styles"]
    chosen=style if style in presets else "auto"
    events=[]
    for item in transcript:
        words=normalize_words(item.get("words", []))
        if not words: continue
        text=str(item.get("text") or " ".join(w.text for w in words)).strip()
        preset=presets.get(chosen, presets["auto"])
        actual_style=chosen
        if chosen == "auto":
            # Let explicit semantic hints win; otherwise use compact word captions for social formats.
            hint=item.get("caption_style")
            actual_style=hint if hint in presets else "word_pop"
            preset=presets[actual_style]
        events.append(CaptionEvent(
            start=float(item.get("start", words[0].start)),
            end=float(item.get("end", words[-1].end)),
            text=text,
            words=words,
            style=actual_style,
            anchor=preset.get("anchor", "bottom_center"),
            animation=preset.get("animation", "fade"),
            emphasis_words=infer_emphasis(words),
            speaker=item.get("speaker")
        ))
    return events


def split_by_timing(event: CaptionEvent, timing: str) -> list[dict[str, Any]]:
    """Produce renderer-ready events for sentence/phrase/word/karaoke/character modes."""
    ws=event.words
    if not ws: return []
    if timing in {"word", "karaoke"}:
        return [{"start":w.start,"end":w.end,"text":event.text,"active_word":i,"mode":timing} for i,w in enumerate(ws)]
    if timing == "character":
        out=[]
        chars=list(event.text)
        total=max(event.end-event.start,0.01)
        step=total/max(len(chars),1)
        for i in range(1,len(chars)+1):
            out.append({"start":event.start+(i-1)*step,"end":event.start+i*step,"text":"".join(chars[:i]),"mode":"character"})
        return out
    if timing == "phrase":
        # Punctuation and short pauses define phrase boundaries.
        groups=[]; current=[]
        for w in ws:
            current.append(w)
            if re.search(r"[,;:!?]$", w.text) or (current and len(current)>=7):
                groups.append(current); current=[]
        if current: groups.append(current)
        return [{"start":g[0].start,"end":g[-1].end,"text":" ".join(x.text for x in g),"mode":"phrase"} for g in groups]
    return [{"start":event.start,"end":event.end,"text":event.text,"mode":"sentence"}]


def export_events(events: list[CaptionEvent], path: str | Path) -> str:
    payload=[]
    for e in events:
        row=asdict(e)
        row["words"]=[asdict(w) for w in e.words]
        payload.append(row)
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)

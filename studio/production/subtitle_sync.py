"""Generate word-timed subtitle JSON from the final narration using faster-whisper."""
from __future__ import annotations
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel


def main():
    audio=Path(sys.argv[1]); out=Path(sys.argv[2]); language=sys.argv[3]
    model=WhisperModel("tiny", device="cpu", compute_type="int8")
    segments,_=model.transcribe(str(audio), language=language, word_timestamps=True, vad_filter=True)
    rows=[]
    for s in segments:
        words=[]
        for w in (s.words or []):
            words.append({"word":w.word.strip(),"start":float(w.start),"end":float(w.end)})
        if words:
            rows.append({"start_time":float(s.start),"end_time":float(s.end),"text":" ".join(x["word"] for x in words),"words":words})
    out.write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__": main()

"""Subtitle QA helpers for SRT/enhanced word-boundary tracks."""
from __future__ import annotations

def validate(items:list[dict], max_lines:int=2, max_words:int=12)->dict:
    findings=[]
    for i,x in enumerate(items):
        text=str(x.get("text","")).strip(); words=text.split()
        if len(words)>max_words: findings.append({"code":"CAPTION_TOO_LONG","index":i,"words":len(words)})
        if float(x.get("end",x.get("end_time",0)))<=float(x.get("start",x.get("start_time",0))):
            findings.append({"code":"INVALID_TIMING","index":i})
        wb=x.get("words") or []
        if wb and len(wb)>max_words: findings.append({"code":"WORD_TRACK_TOO_LONG","index":i})
    return {"ok":not findings,"findings":findings}

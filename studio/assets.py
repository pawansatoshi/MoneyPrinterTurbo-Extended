"""Asset registry and authenticity boundaries."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

class AssetRegistry:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def scan(self) -> list[dict[str, Any]]:
        if not self.root.exists(): return []
        result=[]
        for p in sorted(self.root.rglob("*")):
            if not p.is_file() or p.name.startswith("."): continue
            kind = "video" if p.suffix.lower() in {".mp4",".mov",".webm",".mkv"} else "image" if p.suffix.lower() in {".png",".jpg",".jpeg",".webp"} else "audio" if p.suffix.lower() in {".wav",".mp3",".m4a",".aac"} else "file"
            result.append({"path":str(p),"name":p.stem,"kind":kind,"tags":[],"authentic":False,
                           "source_type":"user_supplied","sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
        return result

    @staticmethod
    def mark_authentic(asset: dict[str, Any], evidence_id: str) -> dict[str, Any]:
        out=dict(asset); out["authentic"]=True; out["source_type"]="official"; out["evidence_ids"]=[evidence_id]
        return out

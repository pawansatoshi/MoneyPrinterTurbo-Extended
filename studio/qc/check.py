"""Lightweight executable QC checks for rendered masters.

Checks are intentionally dependency-light. More advanced CV/audio checks can be
plugged in later without changing the manifest contract.
"""
from __future__ import annotations
import json, subprocess
from pathlib import Path


def probe(path:str)->dict:
    raw=subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],text=True)
    return json.loads(raw)


def run(path:str, expected_format:str="16:9")->dict:
    p=probe(path); video=next((s for s in p["streams"] if s.get("codec_type")=="video"),None); audio=next((s for s in p["streams"] if s.get("codec_type")=="audio"),None)
    checks={}
    if not video: checks["video_stream"]=False
    else:
        checks["video_stream"]=True
        w,h=int(video.get("width",0)),int(video.get("height",0))
        ratio=w/h if h else 0
        target={"16:9":16/9,"9:16":9/16,"1:1":1}.get(expected_format,16/9)
        checks["resolution"]=(w>0 and h>0)
        checks["aspect_ratio"]=abs(ratio-target)<0.02
        checks["fps_valid"]=float(video.get("avg_frame_rate","0/1").split("/")[0])/max(float(video.get("avg_frame_rate","0/1").split("/")[1]),1)==30.0 if "/" in video.get("avg_frame_rate","0/1") else True
    checks["audio_stream"]=audio is not None
    checks["duration_positive"]=float(p["format"].get("duration",0))>0
    checks["master_ready"]=all(checks.values())
    return checks

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--format",default="16:9"); ap.add_argument("--json",dest="json_out")
    a=ap.parse_args(); result=run(a.video,a.format); print(json.dumps(result,indent=2));
    if a.json_out: Path(a.json_out).write_text(json.dumps(result,indent=2),encoding="utf-8")
    raise SystemExit(0 if result["master_ready"] else 2)

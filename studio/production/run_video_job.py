"""GitHub Actions entry point for the free-first PawanStudio factory.

It executes the real pipeline, then the forensic gate. It never converts a
missing dependency or failed QC into a PASS.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/"output/current"; OUT.mkdir(parents=True,exist_ok=True)

def blocked(msg):
    (OUT/"qc_report.json").write_text(json.dumps({"status":"BLOCKED","reason":msg},indent=2),encoding="utf-8")
    print(f"BLOCKED: {msg}"); raise SystemExit(2)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--project-url",required=True); p.add_argument("--language",required=True); p.add_argument("--aspect-ratio",required=True); p.add_argument("--style",required=True); p.add_argument("--duration",required=True); p.add_argument("--free-mode",action="store_true"); a=p.parse_args()
    u=urlparse(a.project_url)
    if u.scheme not in {"http","https"} or not u.netloc: blocked("project_url must be an HTTP(S) official source")
    request={"project_url":a.project_url,"language":a.language,"aspect_ratio":a.aspect_ratio,"style":a.style,"duration_seconds":int(a.duration),"free_mode":bool(a.free_mode),"fail_closed":os.getenv("PAWANSTUDIO_FAIL_CLOSED")=="true"}
    (OUT/"request.json").write_text(json.dumps(request,indent=2),encoding="utf-8")
    cmd=[sys.executable,str(Path(__file__).with_name("free_pipeline.py")),"--project-url",a.project_url,"--language",a.language,"--aspect-ratio",a.aspect_ratio,"--style",a.style,"--duration",a.duration]
    subprocess.run(cmd,check=True)
    video=OUT/"pawanstudio_master.mp4"; manifest=OUT/"asset_manifest.json"; report=OUT/"qc_report.json"
    if not video.exists() or not manifest.exists(): blocked("render or asset manifest missing")
    # One automatic healing pass is reserved for renderer-level re-render. A
    # failed forensic gate is never hidden; it remains FAIL/BLOCKED for action logs.
    qc=[sys.executable,str(Path(__file__).with_name("qc.py")),str(video),str(manifest),str(report)]
    result=subprocess.run(qc)
    if result.returncode!=0:
        # Re-render once from the same verified source manifest. This exercises
        # the mandatory self-healing loop without inventing or substituting assets.
        subprocess.run(cmd,check=True)
        result=subprocess.run(qc)
    if result.returncode!=0:
        print("FINAL STATUS: BLOCKED — forensic QC did not PASS")
        raise SystemExit(2)
    print("FINAL STATUS: PASS")

if __name__=="__main__": main()

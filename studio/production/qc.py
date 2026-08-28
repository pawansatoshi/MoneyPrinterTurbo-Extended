"""Forensic release gate for PawanStudio renders."""
from __future__ import annotations
import json,re,subprocess,sys
from pathlib import Path

def probe(video):
 r=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(video)],capture_output=True,text=True,check=True); return json.loads(r.stdout)
def main():
 video=Path(sys.argv[1]); manifest=Path(sys.argv[2]); report=Path(sys.argv[3]); failures=[]; data=probe(video); streams=data.get("streams",[]); v=next((x for x in streams if x.get("codec_type")=="video"),None); a=next((x for x in streams if x.get("codec_type")=="audio"),None)
 if not v: failures.append("missing video stream")
 else:
  if v.get("width")!=1920 or v.get("height")!=1080: failures.append(f"wrong resolution: {v.get('width')}x{v.get('height')}")
 if not a: failures.append("missing narration/audio stream")
 duration=float(data.get("format",{}).get("duration",0) or 0)
 if duration<3: failures.append("video too short")
 bd=subprocess.run(["ffmpeg","-hide_banner","-i",str(video),"-vf","blackdetect=d=0.5:pix_th=0.98","-an","-f","null","-"],capture_output=True,text=True)
 black=re.findall(r"black_start:([0-9.]+).*?black_end:([0-9.]+).*?black_duration:([0-9.]+)",bd.stderr)
 if black: failures.append(f"unplanned black intervals: {black}")
 try:
  assets=json.loads(manifest.read_text(encoding="utf-8"));
  for x in assets:
   if x.get("source_type")=="official_source_asset" and (not x.get("source_url") or not x.get("sha256")): failures.append("incomplete official asset provenance")
   if x.get("source_type")=="derived_official_asset" and not x.get("derived_from"): failures.append("derived visual missing source hash")
  rm=Path("output/current/render_manifest.json"); rdata=json.loads(rm.read_text(encoding="utf-8")); registered={x.get("asset") for x in assets}
  for s in rdata.get("scenes",[]):
   try: rel=str(Path(s["asset"]).relative_to(Path.cwd()))
   except Exception: rel=str(Path(s["asset"]))
   if rel not in registered: failures.append(f"timeline asset not registered: {rel}")
  if len(rdata.get("scenes",[]))<3: failures.append("insufficient visual scene diversity")
 except Exception as e: failures.append(f"manifest/timeline verification error: {e}")
 script=Path("output/current/script.txt")
 if script.exists():
  txt=script.read_text(encoding="utf-8",errors="ignore")
  for label in ["OFFICIAL SCREENSHOT","OFFICIAL ASSET","ASSET ID","DEBUG","HASH:"]:
   if label in txt: failures.append(f"internal label in narration script: {label}")
 result={"status":"PASS" if not failures else "FAIL","artifact":str(video),"duration_seconds":duration,"failures":failures,"gates":{"technical":not any("resolution" in x or "video stream" in x for x in failures),"audio":not any("audio" in x for x in failures),"black_frames":not any("black" in x for x in failures),"provenance":not any("provenance" in x or "timeline asset" in x for x in failures),"creative_diversity":not any("diversity" in x for x in failures)}}
 report.write_text(json.dumps(result,indent=2),encoding="utf-8"); print(json.dumps(result,indent=2)); raise SystemExit(0 if not failures else 2)
if __name__=="__main__": main()

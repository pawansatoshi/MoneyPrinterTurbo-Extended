"""Free-first PawanStudio production pipeline: research -> evidence -> official capture -> local creative writing -> editorial visual direction -> creator voice -> word subtitles -> render."""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/"output/current"; ASSETS=OUT/"official_assets"; CARDS=OUT/"editorial_cards"
OUT.mkdir(parents=True,exist_ok=True); ASSETS.mkdir(parents=True,exist_ok=True); CARDS.mkdir(parents=True,exist_ok=True)
def sha256(p):
 h=hashlib.sha256();
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
 return h.hexdigest()
def fail(msg):
 (OUT/"qc_report.json").write_text(json.dumps({"status":"BLOCKED","reason":msg},indent=2),encoding="utf-8"); raise SystemExit(2)
def discover_pages(url,limit=6):
 p=urlparse(url)
 if p.scheme not in {"http","https"} or not p.netloc: fail("Invalid official project URL")
 r=requests.get(url,timeout=20,headers={"User-Agent":"PawanStudio/1.0 official-source-research"}); r.raise_for_status(); soup=BeautifulSoup(r.text,"html.parser"); links=[url]
 for a in soup.select("a[href]"):
  u=urljoin(url,a.get("href")).split("#",1)[0]; q=urlparse(u)
  if q.netloc==p.netloc and q.scheme in {"http","https"} and u not in links: links.append(u)
  if len(links)>=limit: break
 return links
def research(url):
 pages=discover_pages(url); rows=[]
 for page in pages:
  try:
   r=requests.get(page,timeout=20,headers={"User-Agent":"PawanStudio/1.0 official-source-research"}); r.raise_for_status(); soup=BeautifulSoup(r.text,"html.parser")
   for x in soup(["script","style","noscript"]): x.decompose()
   rows.append({"url":page,"title":soup.title.get_text(" ",strip=True) if soup.title else "","headings":[x.get_text(" ",strip=True) for x in soup.find_all(["h1","h2","h3"])][:12],"paragraphs":[x.get_text(" ",strip=True) for x in soup.find_all("p") if len(x.get_text(" ",strip=True))>40][:20]})
  except Exception as e: rows.append({"url":page,"error":str(e)})
 (OUT/"research.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding="utf-8"); return rows,pages
def write_script(language,duration):
 subprocess.run([sys.executable,str(Path(__file__).with_name("script_writer.py")),str(OUT/"research.json"),language,str(OUT/"script.txt"),str(duration)],check=True)
def capture(pages):
 js=OUT/"capture_pages.py"; js.write_text('''from playwright.sync_api import sync_playwright\nimport json,sys\nfrom pathlib import Path\npages=json.load(open(sys.argv[1])); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)\nwith sync_playwright() as p:\n b=p.chromium.launch(headless=True); page=b.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)\n for i,u in enumerate(pages):\n  page.goto(u,wait_until="networkidle",timeout=45000); page.screenshot(path=str(out/f"official_{i:02d}.png"),full_page=True)\n b.close()\n''',encoding="utf-8")
 pj=OUT/"pages.json"; pj.write_text(json.dumps(pages),encoding="utf-8"); subprocess.run([sys.executable,str(js),str(pj),str(ASSETS)],check=True); stamp=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()); reg=[]
 for f in sorted(ASSETS.glob("official_*.png")):
  i=int(f.stem.split("_")[-1]); reg.append({"asset":str(f.relative_to(ROOT)),"source_url":pages[i],"retrieved_at":stamp,"source_type":"official_source_asset","asset_role":"first_party_web_capture","sha256":sha256(f)})
 (OUT/"official_asset_manifest.json").write_text(json.dumps(reg,indent=2),encoding="utf-8"); return reg
def make_visuals(reg):
 from studio.production.visual_director import make_cards
 cards=make_cards(reg,CARDS,1920,1080)
 for c in cards: c["asset"]=str(Path(c["asset"]).relative_to(ROOT))
 (OUT/"asset_manifest.json").write_text(json.dumps(reg+cards,indent=2),encoding="utf-8"); return cards
def voice(language):
 ref=ROOT/"reference_audio"/("pawan_english_reference.mp3" if language.lower()=="english" else "pawan_hindi_reference.mp3")
 if not ref.exists(): fail(f"Authorized creator voice reference missing: {ref}")
 refwav=OUT/"voice_reference.wav"; out=OUT/"narration.wav"; subprocess.run(["ffmpeg","-y","-i",str(ref),"-ar","22050","-ac","1",str(refwav)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 lang={"english":"en","hindi":"hi","hinglish":"en"}.get(language.lower(),"en"); code="from TTS.api import TTS; import sys; t=TTS('tts_models/multilingual/multi-dataset/xtts_v2'); t.tts_to_file(text=open(sys.argv[1],encoding='utf-8').read(),file_path=sys.argv[2],speaker_wav=sys.argv[3],language=sys.argv[4])"
 subprocess.run([sys.executable,"-c",code,str(OUT/"script.txt"),str(out),str(refwav),lang],check=True); return out
def subtitles(audio,language):
 out=OUT/"enhanced_subtitles.json"; subprocess.run([sys.executable,str(Path(__file__).with_name("subtitle_sync.py")),str(audio),str(out),{"english":"en","hindi":"hi","hinglish":"en"}.get(language.lower(),"en")],check=True); return out
def manifest(cards,audio,subs,aspect,duration,style):
 res={"16:9":[1920,1080],"1:1":[1080,1080],"9:16":[1080,1920]}[aspect]; per=max(3.0,float(duration)/max(1,len(cards))); cams=["push_in","pan_right","pan_left","drift_left","drift_right","pull_out"]
 scenes=[{"asset":str(ROOT/x["asset"]),"duration":per,"camera":cams[i%len(cams)],"transition":"fade","crop":"cover","role":"evidence_card"} for i,x in enumerate(cards)]
 m={"resolution":res,"fps":30,"bitrate":"9000k","audio_bitrate":"256k","crf":18,"seed":42,"style":style,"scenes":scenes,"audio":str(audio),"enhanced_subtitle":str(subs),"subtitles":{"font_size":54 if aspect=="16:9" else 50,"bottom_margin":90}}
 p=OUT/"render_manifest.json"; p.write_text(json.dumps(m,indent=2),encoding="utf-8"); return p
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--project-url",required=True); ap.add_argument("--language",required=True); ap.add_argument("--aspect-ratio",required=True); ap.add_argument("--style",required=True); ap.add_argument("--duration",required=True); a=ap.parse_args()
 rows,pages=research(a.project_url); subprocess.run([sys.executable,str(Path(__file__).with_name("evidence_ledger.py")),str(OUT/"research.json"),str(OUT/"evidence_ledger.json")],check=True); write_script(a.language,a.duration); reg=capture(pages); cards=make_visuals(reg); audio=voice(a.language); subs=subtitles(audio,a.language); m=manifest(cards,audio,subs,a.aspect_ratio,a.duration,a.style)
 from studio.engine import render; out=OUT/"pawanstudio_master.mp4"; render(m,out); print(out)
if __name__=="__main__": main()

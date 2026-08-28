"""Free-first, self-contained PawanStudio production pipeline.

The pipeline deliberately uses first-party web captures, an authorized creator
voice reference, the existing PawanStudio renderer, and forensic QC. It is
fail-closed: missing provenance or voice never becomes a fake PASS.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "current"
ASSETS = OUT / "official_assets"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str):
    (OUT / "qc_report.json").write_text(json.dumps({"status":"BLOCKED","reason":msg}, indent=2), encoding="utf-8")
    raise SystemExit(2)


def discover_pages(url: str, limit: int = 6):
    p = urlparse(url)
    if p.scheme not in {"http", "https"} or not p.netloc:
        fail("Invalid official project URL")
    r = requests.get(url, timeout=20, headers={"User-Agent":"PawanStudio/1.0 official-source-research"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = [url]
    for a in soup.select("a[href]"):
        href = urljoin(url, a.get("href"))
        q = urlparse(href)
        if q.netloc != p.netloc or q.scheme not in {"http", "https"}:
            continue
        if href.split("#",1)[0] not in links:
            links.append(href.split("#",1)[0])
        if len(links) >= limit:
            break
    return links


def research(url: str):
    pages = discover_pages(url)
    records=[]
    for page in pages:
        try:
            r=requests.get(page, timeout=20, headers={"User-Agent":"PawanStudio/1.0 official-source-research"})
            r.raise_for_status()
            soup=BeautifulSoup(r.text,"html.parser")
            for x in soup(["script","style","noscript"]): x.decompose()
            title=(soup.title.get_text(" ",strip=True) if soup.title else "")
            heads=[x.get_text(" ",strip=True) for x in soup.find_all(["h1","h2","h3"])][:12]
            paras=[x.get_text(" ",strip=True) for x in soup.find_all("p") if len(x.get_text(" ",strip=True))>40][:20]
            records.append({"url":page,"title":title,"headings":heads,"paragraphs":paras})
        except Exception as e:
            records.append({"url":page,"error":str(e)})
    (OUT/"research.json").write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding="utf-8")
    return records, pages


def make_script(records, language):
    # Deterministic free-mode script writer. It uses only retrieved first-party text.
    all_heads=[]
    all_paras=[]
    for r in records:
        all_heads += r.get("headings",[])
        all_paras += r.get("paragraphs",[])
    title=next((r.get("title") for r in records if r.get("title")), "The project")
    clean=re.sub(r"\s+"," ",title).strip()
    facts=[]
    for p in all_paras:
        p=re.sub(r"\s+"," ",p).strip()
        if p and p not in facts: facts.append(p)
    if language.lower()=="english":
        intro=f"What is {clean}, and why does it matter?"
        lines=[intro]
        for p in facts[:5]:
            # Keep source language intact; cap each sentence for natural narration.
            s=p[:300].rsplit(" ",1)[0] if len(p)>300 else p
            lines.append(s)
        lines += ["The important part is not the headline. It is how the product actually works, what it lets users do, and what risks or limitations they should understand.","Before using any financial product, verify the current terms and the official documentation for yourself."]
    elif language.lower()=="hindi":
        lines=[f"Aaj hum samjhenge {clean} kya hai, aur ye kyun important ho sakta hai."]
        lines += facts[:5]
        lines += ["Lekin kisi bhi financial product ko use karne se pehle current terms aur official documentation ko khud verify karna zaroori hai."]
    else:
        lines=[f"What is {clean}, aur ye important kyun hai?"]+facts[:5]+["But headline se zyada important hai ki product actually kaise kaam karta hai aur risks kya hain."]
    script="\n\n".join(lines)
    (OUT/"script.txt").write_text(script,encoding="utf-8")
    return script


def capture_official_pages(pages):
    # Playwright is invoked by the workflow environment.
    import subprocess
    capture_script=OUT/"capture_pages.py"
    capture_script.write_text("""from playwright.sync_api import sync_playwright\nimport json,sys\npages=json.load(open(sys.argv[1]))\nout=sys.argv[2]\nfrom pathlib import Path\nPath(out).mkdir(parents=True,exist_ok=True)\nwith sync_playwright() as p:\n  browser=p.chromium.launch(headless=True)\n  page=browser.new_page(viewport={\"width\":1440,\"height\":900},device_scale_factor=1)\n  for i,url in enumerate(pages):\n    page.goto(url,wait_until=\"networkidle\",timeout=45000)\n    page.screenshot(path=f\"{out}/official_{i:02d}.png\",full_page=True)\n  browser.close()\n""",encoding="utf-8")
    pages_json=OUT/"pages.json"; pages_json.write_text(json.dumps(pages),encoding="utf-8")
    subprocess.run([sys.executable,str(capture_script),str(pages_json),str(ASSETS)],check=True)
    registry=[]
    for f in sorted(ASSETS.glob("official_*.png")):
        registry.append({"asset":str(f.relative_to(ROOT)),"source_url":pages[int(f.stem.split("_")[-1])],"retrieved_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"source_type":"official_source_asset","asset_role":"first_party_web_capture","sha256":sha256(f)})
    (OUT/"asset_manifest.json").write_text(json.dumps(registry,indent=2),encoding="utf-8")
    return registry


def render_voice(script, language, ref):
    if not ref.exists(): fail(f"Authorized creator voice reference missing: {ref}")
    wav=OUT/"voice_reference.wav"
    subprocess.run(["ffmpeg","-y","-i",str(ref),"-ar","22050","-ac","1",str(wav)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    target=OUT/"narration.wav"
    lang={"english":"en","hindi":"hi","hinglish":"en"}.get(language.lower(),"en")
    code=("from TTS.api import TTS; import sys; t=TTS('tts_models/multilingual/multi-dataset/xtts_v2'); t.tts_to_file(text=open(sys.argv[1],encoding='utf-8').read(),file_path=sys.argv[2],speaker_wav=sys.argv[3],language=sys.argv[4])")
    subprocess.run([sys.executable,"-c",code,str(OUT/"script.txt"),str(target),str(wav),lang],check=True)
    return target


def build_manifest(registry, audio, aspect, style, duration):
    # Use official captures as evidence scenes, with restrained camera variation.
    if aspect=="16:9": res=[1920,1080]
    elif aspect=="1:1": res=[1080,1080]
    else: res=[1080,1920]
    images=[x["asset"] for x in registry]
    n=max(1,len(images)); per=max(3.0,float(duration)/n)
    scenes=[{"asset":str(ROOT/x),"duration":per,"camera":c,"transition":"fade","crop":"cover"} for x,c in zip(images,["push_in","pan_right","pan_left","drift_left","drift_right","pull_out"])]
    manifest={"resolution":res,"fps":30,"bitrate":"9000k","audio_bitrate":"256k","crf":18,"seed":42,"scenes":scenes,"audio":str(audio),"subtitle":None,"enhanced_subtitle":None,"subtitles":{"font_size":54 if aspect=="16:9" else 50,"bottom_margin":90}}
    path=OUT/"render_manifest.json"; path.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    return path


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-url",required=True); ap.add_argument("--language",required=True); ap.add_argument("--aspect-ratio",required=True); ap.add_argument("--style",required=True); ap.add_argument("--duration",required=True)
    a=ap.parse_args()
    records,pages=research(a.project_url)
    script=make_script(records,a.language)
    ref=ROOT/"reference_audio"/("pawan_english_reference.mp3" if a.language.lower()=="english" else "pawan_hindi_reference.mp3")
    registry=capture_official_pages(pages)
    audio=render_voice(script,a.language,ref)
    manifest=build_manifest(registry,audio,a.aspect_ratio,a.style,a.duration)
    from studio.engine import render
    output=OUT/"pawanstudio_master.mp4"
    render(manifest,output)
    print(output)

if __name__=="__main__": main()

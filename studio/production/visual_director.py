"""Generate editorial visual cards from verified first-party captures.

No product UI is redrawn. Cards only crop, blur, frame and annotate authentic
captures or create clearly conceptual typography/diagram cards.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json


def font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def fit(im,size):
    scale=max(size[0]/im.width,size[1]/im.height); im=im.resize((int(im.width*scale),int(im.height*scale)))
    return im.crop(((im.width-size[0])//2,(im.height-size[1])//2,(im.width+size[0])//2,(im.height+size[1])//2))

def make_cards(asset_manifest, out_dir, width=1920,height=1080):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); entries=[]
    for i,item in enumerate(asset_manifest):
        src=Path(item["asset"]); im=Image.open(src).convert("RGB")
        bg=fit(im,(width,height)).filter(ImageFilter.GaussianBlur(18)).resize((width,height))
        canvas=bg.copy(); overlay=Image.new("RGBA",canvas.size,(0,0,0,115)); canvas=Image.alpha_composite(canvas.convert("RGBA"),overlay)
        card=fit(im,(int(width*.78),int(height*.72))).convert("RGBA")
        canvas.alpha_composite(card,((width-card.width)//2,(height-card.height)//2+45))
        d=ImageDraw.Draw(canvas); title=item.get("source_url","").rstrip("/").split("/")[-1].replace("-"," ").replace("_"," ").title() or "Product walkthrough"
        d.text((90,70),title,font=font(54),fill=(255,255,255,255),stroke_width=2,stroke_fill=(0,0,0,180))
        d.text((90,height-105),f"{i+1:02d}",font=font(42),fill=(255,255,255,220))
        path=out/f"scene_{i:02d}.png"; canvas.convert("RGB").save(path,quality=95)
        entries.append({"asset":str(path),"source_url":item["source_url"],"source_type":"derived_official_asset","derived_from":item["sha256"],"asset_role":"editorial_crop_card"})
    return entries

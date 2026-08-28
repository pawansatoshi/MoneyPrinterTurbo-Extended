"""Build a first-party claim/evidence ledger from retrieved research."""
from __future__ import annotations
import json,sys
from pathlib import Path

def main():
 src=Path(sys.argv[1]); out=Path(sys.argv[2]); rows=json.loads(src.read_text(encoding="utf-8")); claims=[]
 for r in rows:
  url=r.get("url")
  for p in r.get("paragraphs",[]):
   p=" ".join(p.split())
   if len(p)>=40: claims.append({"claim":p,"source_url":url,"source_type":"first_party","retrieved":True,"confidence":"source-backed","time_sensitive":any(x in p.lower() for x in ["today","current","rate","apy","launch","liquidity","minutes"])})
 out.write_text(json.dumps({"claims":claims},indent=2,ensure_ascii=False),encoding="utf-8")
if __name__=="__main__": main()

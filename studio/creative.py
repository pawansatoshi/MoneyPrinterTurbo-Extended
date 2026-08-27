"""Creative intelligence primitives: hooks, re-hooks, metaphors and metadata."""
from __future__ import annotations
import re

HOOKS={"launch":["Something important just changed.","The launch is closer than it looks.","Here is what most people are missing."],
       "explainer":["Most people misunderstand this.","Here is the simple version.","The surprising part is what happens next."],
       "demo":["Watch what happens when we do this.","This is the part worth seeing."]}

class CreativeDirector:
    def __init__(self, seed:int=42): self.seed=seed
    def hooks(self, template:str="explainer", count:int=3):
        vals=HOOKS.get(template,HOOKS["explainer"]); return [vals[(self.seed+i)%len(vals)] for i in range(min(count,len(vals)))]
    def rehooks(self, script:str):
        sentences=[s.strip() for s in re.split(r"(?<=[.!?])\s+",script) if s.strip()]
        return [f"But here is the catch: {s}" for s in sentences[2::3]]
    def metadata(self, topic:str, script:str):
        clean=re.sub(r"[^\w\s]"," ",topic).strip(); words=clean.split()
        hashtags=["#"+w for w in words if len(w)>2][:8]+["#Video","#Explainer"]
        return {"title_options":[topic, f"What {topic} Actually Means", f"{topic}: The Part Nobody Explains"],
                "description":script[:500].strip(),"hashtags":hashtags}

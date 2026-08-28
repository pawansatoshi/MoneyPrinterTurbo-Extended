"""Free local script writer using Qwen2.5-0.5B-Instruct.

The model is constrained to the retrieved first-party research text; it is a
writer, not a source of facts. The raw evidence is preserved in research.json.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL="Qwen/Qwen2.5-0.5B-Instruct"

def _normalise_template_output(inp):
    """Return tensor-like input_ids plus an optional attention mask.

    Transformers versions differ in whether apply_chat_template returns a
    Tensor or a BatchEncoding. Never access `.shape` on the container itself.
    """
    if hasattr(inp, "input_ids"):
        input_ids = inp.input_ids
        attention_mask = getattr(inp, "attention_mask", None)
    elif isinstance(inp, dict) and "input_ids" in inp:
        input_ids = inp["input_ids"]
        attention_mask = inp.get("attention_mask")
    else:
        input_ids = inp
        attention_mask = None
    if not hasattr(input_ids, "shape"):
        raise TypeError("Tokenizer did not return tensor-like input_ids")
    return input_ids, attention_mask

def main():
 research=Path(sys.argv[1]); language=sys.argv[2]; out=Path(sys.argv[3]); duration=int(sys.argv[4])
 rows=json.loads(research.read_text(encoding="utf-8")); evidence=[]
 for r in rows:
  if r.get("title"): evidence.append("TITLE: "+r["title"])
  for h in r.get("headings",[]): evidence.append("HEADING: "+h)
  for p in r.get("paragraphs",[])[:8]: evidence.append("FACT: "+p)
 evidence="\n".join(evidence)[:14000]
 prompt=f'''You are an expert educational YouTube writer. Write a concise, natural {language} narration for about {duration} seconds. Use ONLY facts present in the evidence below. Do not invent rates, dates, partnerships, numbers, launches, guarantees, or product capabilities. Structure it as HOOK, QUESTION, EXPLANATION, HOW IT WORKS, WHY IT MATTERS, RISK/QUALIFIER, PAYOFF. Make it conversational and varied, not corporate. Do not mention sources, asset labels, or that you are an AI.\n\nEVIDENCE:\n{evidence}'''
 tok=AutoTokenizer.from_pretrained(MODEL); model=AutoModelForCausalLM.from_pretrained(MODEL)
 msgs=[{"role":"system","content":"You write accurate educational video narration and never invent facts."},{"role":"user","content":prompt}]
 inp=tok.apply_chat_template(msgs,add_generation_prompt=True,return_tensors="pt")
 input_ids, attention_mask = _normalise_template_output(inp)
 kwargs={"input_ids":input_ids,"max_new_tokens":max(220,min(700,duration*3)),"do_sample":True,"temperature":0.65,"top_p":0.9}
 if attention_mask is not None: kwargs["attention_mask"]=attention_mask
 pad_id=getattr(tok,"pad_token_id",None)
 if pad_id is not None: kwargs["pad_token_id"]=pad_id
 out_ids=model.generate(**kwargs)
 text=tok.decode(out_ids[0][input_ids.shape[-1]:],skip_special_tokens=True).strip()
 if not text: raise SystemExit("Local script model returned empty output")
 out.write_text(text,encoding="utf-8")
if __name__=="__main__": main()

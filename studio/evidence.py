"""Evidence ledger for claim-safe product storytelling."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class Evidence:
    id:str
    claim:str
    source:str
    locator:str=""
    verified:bool=False

class EvidenceLedger:
    def __init__(self, items:list[dict[str,Any]]|None=None):
        self.items={x["id"]:Evidence(**x) for x in (items or []) if "id" in x}
    def add(self, item:dict[str,Any]):
        e=Evidence(**item); self.items[e.id]=e; return asdict(e)
    def verify(self, evidence_id:str):
        e=self.items[evidence_id]; self.items[evidence_id]=Evidence(e.id,e.claim,e.source,e.locator,True)
    def claims(self, ids:list[str]):
        return [asdict(self.items[i]) for i in ids if i in self.items]
    def unresolved(self, ids:list[str]):
        return [i for i in ids if i not in self.items or not self.items[i].verified]

"""Deterministic creative planner.

Turns a brief into a structured, editable production plan. It deliberately does
not invent factual product claims; factual copy must arrive from research or a
project-approved script.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

DIRECTOR_DEFAULTS={
    "cinematic":["hook","tension","reveal","payoff","cta"],
    "product_demo":["hook","problem","feature","interaction","result","cta"],
    "tech_explainer":["hook","question","mechanism","example","implication","cta"],
    "documentary":["hook","context","evidence","human_story","conclusion"],
    "launch_hype":["hook","countdown","reveal","proof","cta"],
    "news":["hook","what","evidence","why","impact","next"],
    "talking_head":["hook","statement","support","statement","payoff"],
    "podcast":["hook","context","best_moment","takeaway"],
    "motion_graphics":["setup","build","emphasis","resolve"],
    "gaming":["hook","action","reaction","payoff"],
    "shorts":["hook","value","pattern_break","cta"],
    "localization":["preserve_story","translate","re_time","reframe"],
}

@dataclass
class Beat:
    id:str
    purpose:str
    visual_mode:str
    caption_mode:str
    camera:str
    transition:str


def choose_visual(beat:str, primary:str) -> str:
    if beat in {"hook","reveal","payoff"}: return "kinetic_typography"
    if primary=="product_demo" and beat in {"feature","interaction","result"}: return "real_ui"
    if beat in {"evidence","what"}: return "source_card"
    if beat in {"mechanism","example"}: return "diagram"
    if beat in {"statement","support","human_story","best_moment"}: return "talking_head_or_broll"
    return "broll_or_graphic"


def choose_caption(beat:str) -> str:
    if beat=="hook": return "hook"
    if beat in {"reveal","payoff","countdown","emphasis"}: return "emphasis"
    if beat in {"feature","interaction","result","mechanism"}: return "word_pop"
    return "minimal"


def choose_camera(visual:str) -> str:
    return {
        "real_ui":"ui_region_follow",
        "diagram":"beat_zoom",
        "source_card":"push_in",
        "talking_head_or_broll":"subject_follow",
        "kinetic_typography":"static",
        "broll_or_graphic":"parallax",
    }.get(visual,"static")


def choose_transition(i:int, visual:str) -> str:
    if i==0: return "fade"
    if visual=="real_ui": return "match_cut"
    if visual=="kinetic_typography": return "whip"
    return "crossfade"


def plan(brief:dict[str,Any]) -> dict[str,Any]:
    primary=brief.get("director",{}).get("primary","product_demo")
    mix=brief.get("director",{}).get("mix",[])
    beats=brief.get("story",{}).get("beats") or DIRECTOR_DEFAULTS.get(primary,DIRECTOR_DEFAULTS["product_demo"])
    out=[]
    for i,b in enumerate(beats):
        visual=choose_visual(b,primary)
        out.append(asdict(Beat(b,b,visual,choose_caption(b),choose_camera(visual),choose_transition(i,visual))))
    return {"schema_version":"1.0","director":{"primary":primary,"mix":mix},"beats":out,"rules":["official_product_assets_for_product_claims","no_fabricated_ui","preserve_asset_provenance","run_qc_before_master"]}

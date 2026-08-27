"""Composable style mixer: attributes, not imitation of living creators."""
from __future__ import annotations

STYLE_PROFILES={
 "premium_cinematic":{"pacing":"medium","camera":"restrained","typography":"minimal","transitions":"match_cut","music":"minimal_electronic"},
 "high_retention":{"pacing":"fast","camera":"beat_driven","typography":"social_bold","transitions":"pattern_break","music":"energetic"},
 "documentary":{"pacing":"slow","camera":"observational","typography":"lower_third","transitions":"cut","music":"ambient"},
 "tech_clean":{"pacing":"medium","camera":"ui_region_follow","typography":"technical","transitions":"clean","music":"minimal"},
 "launch_energy":{"pacing":"fast","camera":"hero_reveal","typography":"kinetic","transitions":"impact","music":"riser_impact"},
 "podcast_social":{"pacing":"fast","camera":"subject_follow","typography":"social_highlight","transitions":"punch","music":"low_bed"},
 "newsroom":{"pacing":"fast","camera":"stable","typography":"news_broadcast","transitions":"cut","music":"news_bed"}
}

def mix(profiles:list[str], overrides:dict|None=None)->dict:
    selected=[STYLE_PROFILES[p] for p in profiles if p in STYLE_PROFILES]
    result={}
    for item in selected:
        result.update(item)
    if overrides: result.update(overrides)
    result["profiles"]=[p for p in profiles if p in STYLE_PROFILES]
    return result

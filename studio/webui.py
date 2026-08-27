"""Optional Streamlit Studio UI. Run: streamlit run studio/webui.py"""
from __future__ import annotations
import json, tempfile
from pathlib import Path
import streamlit as st
from studio.director import MasterDirector
from studio.qc import QualityGate
from studio.platforms import PROFILES

st.set_page_config(page_title="Pawan Video Studio", layout="wide")
st.title("Pawan Video Studio")
st.caption("Brief → Director → Evidence-aware plan → QC → Render")

with st.sidebar:
    template=st.selectbox("Template", ["launch","explainer","demo","announcement","comparison","documentary"])
    platform=st.selectbox("Output", list(PROFILES))
    seed=st.number_input("Creative seed", min_value=0, value=42, step=1)
    duration=st.number_input("Scene duration", min_value=1.0, value=4.0, step=.5)

topic=st.text_input("Topic", "Sats Terminal")
script=st.text_area("Narration / script", height=220)
assets_text=st.text_area("Asset registry JSON (optional)", "[]", height=120)
col1,col2=st.columns(2)
with col1:
    if st.button("Build plan", use_container_width=True):
        try:
            assets=json.loads(assets_text)
            brief={"project":topic.lower().replace(" ","-"),"topic":topic,"script":script,"template":template,
                   "assets":assets,"scene_duration":duration,"resolution":[PROFILES[platform].width,PROFILES[platform].height]}
            manifest=MasterDirector(seed=int(seed)).plan(brief)
            manifest["quality"]=QualityGate().check(manifest)
            st.session_state["manifest"]=manifest
        except Exception as exc: st.error(str(exc))
with col2:
    if st.button("Run QC", use_container_width=True) and "manifest" in st.session_state:
        st.json(QualityGate().check(st.session_state["manifest"]))

if "manifest" in st.session_state:
    manifest=st.session_state["manifest"]
    st.subheader("Director plan")
    for shot in manifest["shots"]:
        with st.expander(f"{shot['id']} · {shot['beat']} · {shot['camera']}"):
            st.write(shot["narration"])
            st.caption(f"Asset: {shot['asset'] or 'conceptual fallback'} · source: {shot['source_type']}")
    st.download_button("Export manifest", json.dumps(manifest,ensure_ascii=False,indent=2), "studio-project.json", "application/json")

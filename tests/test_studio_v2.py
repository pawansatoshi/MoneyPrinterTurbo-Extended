from studio.director import MasterDirector
from studio.qc import QualityGate
from studio.platforms import profile

def test_director_is_deterministic():
    brief={"topic":"Test","script":"One. Two. Three. Four.","template":"explainer"}
    assert MasterDirector(7).plan(brief)==MasterDirector(7).plan(brief)

def test_authenticity_is_preserved():
    brief={"topic":"Product","script":"The official dashboard shows the balance.","template":"demo",
           "assets":[{"path":"/missing/dashboard.png","name":"dashboard","description":"official dashboard balance","authentic":True,"evidence_ids":["official-1"]}]}
    plan=MasterDirector().plan(brief)
    assert any(s["source_type"]=="authentic" for s in plan["shots"])
    assert all("fake" not in str(s).lower() for s in plan["shots"])

def test_qc_flags_missing_shots():
    report=QualityGate().check({"resolution":[1080,1920],"shots":[]})
    assert not report["ok"]

def test_platform_profile():
    assert profile("shorts")["width"]==1080
    assert profile("shorts")["height"]==1920

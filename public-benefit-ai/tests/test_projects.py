import pytest
from app.catalog import PROJECTS
from app.engine import process
from app.retrieval import retrieve
from app.forecasting import forecast
from app.spatial import hotspots
from app.records import duplicate_review
from app.classification import suspicious_link_indicators

@pytest.mark.parametrize("slug",list(PROJECTS))
def test_all_ten_projects_run(slug):
    result=process(slug,{"text":"Please check this flood eligibility road incident footpath account message"})
    assert result["demo_mode"] is True
    assert result["project"] == PROJECTS[slug][0]
    assert "result" in result

def test_rag_abstains_without_relevant_sources():
    assert retrieve("quantum entanglement",[{"id":"a","title":"Library hours","text":"Books","status":"synthetic"}])["abstained"]

def test_health_red_flag_does_not_diagnose():
    x=process("trusted-public-health-information-assistant",{"text":"chest pain"})
    assert x["result"]["escalation"] is True
    assert not x["result"]["citations"]

def test_no_fabricated_active_disaster_alerts():
    x=process("ai-disaster-response-public-safety-assistant",{"text":"flood preparedness"})
    assert x["demo_mode"] and "alerts" not in x

def test_forecast_has_chronological_baseline():
    x=forecast(list(range(1,17)),"illustrative_rainfall")
    assert x["holdout_n"]>0 and x["persistence_baseline_mae"]>=0

def test_bad_forecast_input_rejected():
    with pytest.raises(ValueError):forecast([1,2],"pm25")

def test_bad_spatial_coordinates_rejected():
    with pytest.raises(ValueError):hotspots([{"latitude":120,"longitude":0}])

def test_private_match_never_auto_merges():
    x=duplicate_review({"description_tags":"blue bag bus terminal"},[{"reference_code":"DEMO-101","description_tags":"blue bag bus terminal"}])
    assert x["suggestions"] and not x["merged"] and not x["matched_identity"]

def test_scam_urls_are_not_visited():
    x=process("scam-phishing-awareness-assistant",{"text":"urgent password https://xn--abc.test"})
    assert x["result"]["urls_visited"] is False
    assert x["result"]["url_indicators"]

def test_unknown_project_rejected():
    with pytest.raises(KeyError):process("fake-project",{})

def test_ticket_moderation():
    x=process("accessibility-civic-issue-reporting",{"text":"streetlight broken"})
    assert x["result"]["needs_human_moderation"]

def test_no_medical_guidance_with_missing_support():
    x=process("trusted-public-health-information-assistant",{"text":"what is a quasar"})
    assert x["result"]["abstained"]

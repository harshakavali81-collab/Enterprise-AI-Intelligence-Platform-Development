"""Contract and safety regression tests for all ten demonstration engines."""
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.catalog import PROJECTS
from app.engine import process
from app.records import duplicate_review
from app.forecasting import forecast
from app.classification import suspicious_link_indicators

ROOT=Path(__file__).resolve().parents[1]
client=TestClient(app)

@pytest.mark.parametrize("slug",list(PROJECTS))
def test_individual_examples_round_trip_over_http(slug):
    raw=(ROOT/"projects"/slug/"sample_request.json").read_text(encoding="utf8")
    request=json.loads(raw)
    response=client.post(f"/api/v1/{slug}/analyze",json=request)
    assert response.status_code==200, response.text
    data=response.json()
    assert data["slug"]==slug
    assert data["demo_mode"] is True
    assert data["data_provenance"]
    assert "safety_notice" in data
    assert isinstance(data["result"],dict)

@pytest.mark.parametrize("slug",list(PROJECTS))
def test_too_large_user_input_is_rejected_for_each_project(slug):
    response=client.post(f"/api/v1/{slug}/analyze",json={"text":"x"*31000})
    assert response.status_code==413

def test_rag_abstains_for_empty_input():
    x=process("ai-disaster-response-public-safety-assistant",{"text":""})
    assert x["result"]["abstained"] is True
    assert not x["result"]["citations"]

def test_urgent_medical_question_escalates_without_synthetic_document_citations():
    x=process("trusted-public-health-information-assistant",{"text":"difficulty breathing"})
    assert x["result"]["escalation"] is True
    assert x["result"]["citations"]==[]

def test_nonnegative_pm25_and_no_fake_pollution_reading():
    with pytest.raises(ValueError):
        forecast([1,2,3,4,5,-7,8,9],"pm25")
    x=process("air-quality-environmental-health-monitor",{})
    assert x["demo_mode"] and x["result"]["data_origin"]=="caller-provided or synthetic fixture"

def test_missing_person_matches_cannot_merge_automatically():
    x=duplicate_review({"description_tags":"blue bag bus terminal"},[{"reference_code":"DEMO-123","description_tags":"blue bag bus terminal"}])
    assert not x["merged"] and not x["matched_identity"]
    assert all(v["requires_human_review"] for v in x["suggestions"])

def test_unsafe_link_parser_returns_indicators_not_network_responses():
    urls=suspicious_link_indicators("verify now http://test.example/signin and https://xn--sample.test/path")
    assert len(urls)==2
    assert any("unencrypted_scheme" in v["indicators"] for v in urls)
    assert all("body" not in v and "download" not in v for v in urls)

def test_approved_cors_only_allows_local_demo_browser():
    allowed=client.options(
        "/api/v1/projects",
        headers={"origin":"http://127.0.0.1:5173","access-control-request-method":"GET"}
    )
    assert allowed.headers.get("access-control-allow-origin")=="http://127.0.0.1:5173"
    rejected=client.options(
        "/api/v1/projects",
        headers={"origin":"https://malicious.example","access-control-request-method":"GET"}
    )
    assert rejected.headers.get("access-control-allow-origin") is None

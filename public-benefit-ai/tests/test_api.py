from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    assert client.get("/health").json()["status"]=="ok"
def test_catalog_has_ten():
    assert len(client.get("/api/v1/projects").json())==10
def test_post_analysis():
    r=client.post("/api/v1/scam-phishing-awareness-assistant/analyze",json={"text":"verify OTP immediately"})
    assert r.status_code==200 and r.json()["demo_mode"]
def test_invalid_slug():
    assert client.post("/api/v1/unknown/analyze",json={}).status_code==404
def test_too_short_forecast_rejected():
    assert client.post("/api/v1/ai-flood-disaster-early-warning/analyze",json={"observations":[1,2]}).status_code==422

import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app,PROJECT_SLUG
client=TestClient(app)
def test_sample(): 
    p=json.loads(Path("sample_request.json").read_text())
    r=client.post("/api/v1/analyze",json=p)
    assert r.status_code==200,r.text
    assert r.json()["slug"]==PROJECT_SLUG and r.json()["demo_mode"]
    assert r.json()["result"]["needs_human_moderation"]
def test_health_and_sources():
    assert client.get("/health").json()["project"]==PROJECT_SLUG
    assert client.get("/api/v1/sources").status_code==200
def test_payload_limit():
    assert client.post("/api/v1/analyze",json={"text":"x"*35000}).status_code==413

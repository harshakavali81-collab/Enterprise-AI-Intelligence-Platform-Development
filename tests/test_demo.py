import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app,PROJECT_SLUG
from app.engine import process
client=TestClient(app)
def test_health_and_source():
    assert client.get("/health").json()["project"]==PROJECT_SLUG
    assert client.get("/api/v1/sources").status_code==200
def test_sample_api():
    sample=json.loads(Path("sample_request.json").read_text())
    r=client.post("/api/v1/analyze",json=sample)
    assert r.status_code==200,r.text
    assert r.json()["slug"]==PROJECT_SLUG and r.json()["demo_mode"]
def test_oversized():
    assert client.post("/api/v1/analyze",json={"text":"x"*35000}).status_code==413

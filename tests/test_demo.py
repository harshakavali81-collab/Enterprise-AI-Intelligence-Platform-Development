import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app, PROJECT_SLUG
from app.engine import process
client=TestClient(app)
def test_health_and_sources():
    assert client.get("/health").json()["project"]==PROJECT_SLUG
    assert client.get("/api/v1/sources").status_code==200
def test_project_api():
    obj=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    resp=client.post("/api/v1/analyze",json=obj)
    assert resp.status_code==200,resp.text
    d=resp.json()
    assert d["slug"]==PROJECT_SLUG and d["demo_mode"]
def test_reject_large_input():
    assert client.post("/api/v1/analyze",json={"text":"x"*35000}).status_code==413
def test_synthetic_provenance():
    obj=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    result=process(PROJECT_SLUG,obj)
    assert "synthetic" in result["data_provenance"].lower()

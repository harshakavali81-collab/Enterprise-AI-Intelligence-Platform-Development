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
    response=client.post("/api/v1/analyze",json=obj)
    assert response.status_code==200,response.text
    data=response.json()
    assert data["slug"]==PROJECT_SLUG and data["demo_mode"]
def test_reject_oversized_input():
    assert client.post("/api/v1/analyze",json={"text":"x"*35000}).status_code==413
def test_no_real_world_impersonation():
    obj=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    d=process(PROJECT_SLUG,obj)
    assert d["data_provenance"].lower().startswith("synthetic")

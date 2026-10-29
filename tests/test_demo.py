import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app,PROJECT_SLUG
from app.engine import process
client=TestClient(app)
def test_health():
    assert client.get("/health").json()["project"]==PROJECT_SLUG
    assert client.get("/api/v1/sources").status_code==200
def test_fixture():
    obj=json.loads(Path("sample_request.json").read_text())
    r=client.post("/api/v1/analyze",json=obj)
    assert r.status_code==200,r.text
    assert r.json()["slug"]==PROJECT_SLUG and r.json()["demo_mode"] is True
def test_input_rejected():
    assert client.post("/api/v1/analyze",json={"text":"x"*33000}).status_code==413

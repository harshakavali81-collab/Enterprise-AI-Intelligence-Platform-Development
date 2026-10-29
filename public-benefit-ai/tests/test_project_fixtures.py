"""Every detailed project has its own executable sample contract."""
from pathlib import Path
import json
import pytest
from app.catalog import PROJECTS
from app.engine import process

@pytest.mark.parametrize("slug",list(PROJECTS))
def test_each_project_fixture(slug):
    path = Path(__file__).resolve().parents[1] / "projects" / slug
    assert (path / "README.md").is_file()
    assert (path / "assets" / "cover.svg").is_file()
    payload = json.loads((path / "sample_request.json").read_text())
    result = process(slug,payload)
    assert result["slug"] == slug
    assert result["demo_mode"] is True
    assert "result" in result

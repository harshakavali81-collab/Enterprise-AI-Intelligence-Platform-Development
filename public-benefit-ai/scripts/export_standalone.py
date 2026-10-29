#!/usr/bin/env python3
"""Export ten fully standalone, titled GitHub-ready repositories.

From public-benefit-ai/:
 python scripts/export_standalone.py
 python scripts/export_standalone.py --publish

--publish needs git, gh and an authenticated GitHub account with permissions to
create repositories. It never overwrites an existing destination repository.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"dist"/"independent-repositories"
OWNER="harshakavali81-collab"
TITLES={
"ai-disaster-response-public-safety-assistant":"AI-Disaster-Response-and-Public-Safety-Assistant",
"ai-flood-disaster-early-warning":"AI-Flood-and-Natural-Disaster-Early-Warning-Support",
"emergency-services-coordination-copilot":"Emergency-Services-Information-and-Coordination-Copilot",
"trusted-public-health-information-assistant":"Trusted-Public-Health-Information-Assistant",
"ai-road-safety-hotspot-intelligence":"AI-Road-Safety-and-Accident-Hotspot-Intelligence",
"scam-phishing-awareness-assistant":"AI-Scam-Phishing-and-Digital-Fraud-Awareness-Assistant",
"multilingual-civic-services-navigator":"Multilingual-Civic-Services-and-Government-Scheme-Navigator",
"privacy-preserving-missing-person-coordination":"Privacy-Preserving-Missing-Person-Information-Coordination",
"air-quality-environmental-health-monitor":"AI-Air-Quality-and-Environmental-Health-Monitor",
"accessibility-civic-issue-reporting":"AI-Accessibility-and-Civic-Issue-Reporting-Platform",
}

MAIN='''"""Independent API for one public-benefit AI demonstration."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from app.engine import process

PROJECT_SLUG = "__SLUG__"
app=FastAPI(title="__TITLE__",version="0.1.0",description="Synthetic portfolio demonstration, not a live public-safety service")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],
                   allow_methods=["GET","POST"],allow_headers=["Content-Type"])

@app.get("/health")
def health():
    return {"status":"ok","demo_mode":True,"project":PROJECT_SLUG}

@app.post("/api/v1/analyze")
def analyze(body:dict[str,Any]):
    if len(str(body))>30000:
        raise HTTPException(status_code=413,detail="Payload too large")
    try:
        return process(PROJECT_SLUG,body)
    except (KeyError,ValueError,TypeError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc
'''
TEST='''import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app, PROJECT_SLUG
from app.engine import process

def test_fixture_is_runnable():
    sample=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    result=process(PROJECT_SLUG,sample)
    assert result["demo_mode"]
    assert result["slug"]==PROJECT_SLUG

def test_api_contract():
    client=TestClient(app)
    assert client.get("/health").status_code==200
    sample=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    assert client.post("/api/v1/analyze",json=sample).status_code==200
    assert client.post("/api/v1/analyze",json={"text":"x"*31000}).status_code==413
'''
CI='''name: Standalone synthetic demo tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python -m pytest -q
'''
def run(cmd:list[str],cwd:Path|None=None,check:bool=True):
    return subprocess.run(cmd,cwd=cwd,check=check,text=True)

def export_one(slug:str,name:str,replace:bool=False)->Path:
    folder=OUT/name
    if folder.exists() and replace:
        shutil.rmtree(folder)
    if folder.exists():
        raise FileExistsError(f"Refusing to overwrite: {folder}. Use --replace.")
    folder.mkdir(parents=True)
    # Isolated clone of essential code, not a symlink to the parent repository.
    shutil.copytree(ROOT/"app",folder/"app",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    shutil.copytree(ROOT/"projects"/slug/"assets",folder/"assets")
    shutil.copytree(ROOT/"projects"/slug/"docs",folder/"docs")
    for file in ("requirements.txt","Dockerfile","docker-compose.yml",".gitignore",".env.example"):
        shutil.copy2(ROOT/file,folder/file)
    shutil.copy2(ROOT/"projects"/slug/"sample_request.json",folder/"sample_request.json")
    shutil.copy2(ROOT/"projects"/slug/"cli.py",folder/"cli.py")
    # Adapt CLI from its original parent-directory location for standalone execution.
    (folder/"cli.py").write_text(
        '''import json
from pathlib import Path
from app.engine import process
from app.main import PROJECT_SLUG
if __name__=="__main__":
    data=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    print(json.dumps(process(PROJECT_SLUG,data),indent=2))
''',encoding="utf8")
    (folder/"app"/"main.py").write_text(MAIN.replace("__SLUG__",slug).replace("__TITLE__",name.replace("-"," ")),encoding="utf8")
    # Copy the interactive browser UI and scope the project list to this repository.
    ui_folder=folder/"frontend"
    ui_folder.mkdir()
    source_ui=(ROOT/"frontend"/"index.html").read_text(encoding="utf8")
    # The collection frontend embeds a line: const projects=<JSON>;
    import re
    single_project=json.dumps([{"slug":slug,"name":name.replace("-"," "),"example":json.loads((folder/"sample_request.json").read_text(encoding="utf8"))}])
    source_ui=re.sub(r'const projects=.*?;',lambda _m:"const projects="+single_project+";",source_ui,count=1)
    source_ui=source_ui.replace('"http://127.0.0.1:8000/api/v1/"+projects[active].slug+"/analyze"',
                                '"http://127.0.0.1:8000/api/v1/analyze"')
    (ui_folder/"index.html").write_text(source_ui,encoding="utf8")

    (folder/"tests").mkdir()
    (folder/"tests"/"test_demo.py").write_text(TEST,encoding="utf8")
    (folder/"pytest.ini").write_text("[pytest]\npythonpath = .\ntestpaths = tests\n",encoding="utf8")
    (folder/".github"/"workflows").mkdir(parents=True)
    (folder/".github"/"workflows"/"ci.yml").write_text(CI,encoding="utf8")
    content=(ROOT/"projects"/slug/"README.md").read_text(encoding="utf8")
    content=content.replace("(assets/cover.svg)","(assets/cover.svg)")
    content=content.replace("(sample_request.json)","(sample_request.json)")
    content=content.replace("python projects/"+slug+"/cli.py","python cli.py")
    content=content.replace("POST /api/v1/"+slug+"/analyze","POST /api/v1/analyze")
    content=content.replace("Path: `projects/"+slug+"`","Path: this standalone repository")
    content=content.replace("`../../app/`","`app/`").replace("`../../tests/`","`tests/`").replace("`../../Dockerfile`","`Dockerfile`")
    content=content.replace("`../../scripts/evaluate.py`","per-project tests in `tests/`")
    content=content.replace("`../../frontend/index.html`","`frontend/index.html`")
    content=content.replace("([Acceptance criteria](../../docs/ACCEPTANCE.md))","(see below)")
    content=content.replace("[Acceptance criteria](../../docs/ACCEPTANCE.md)","additional validation required before real-world use")
    content=content.replace("[All ten projects](../INDEX.md)","[Project collection](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/main/public-benefit-ai/projects)")
    content += "\n\n## Independent repository entrypoint\n\nThis repository is an independent export, with its own backend, interactive frontend, synthetic fixtures, tests, Dockerfile and workflows. Run `python cli.py` or `uvicorn app.main:app`. The API route is `POST /api/v1/analyze`. Shared baseline source modules are copied so the project does not depend on the parent repo. Run `python -m http.server 5173 --directory frontend` in another terminal to open the local interface. Not production validated.\n"
    (folder/"README.md").write_text(content,encoding="utf8")
    (folder/"PROJECT.json").write_text(json.dumps({"title":name.replace("-"," "),"slug":slug,"mode":"synthetic demonstration","operational_status":"not production ready"},indent=2)+"\n",encoding="utf8")
    return folder

def publish_one(folder:Path,name:str):
    dest=f"{OWNER}/{name}"
    status=subprocess.run(["gh","repo","view",dest],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if status.returncode==0:
        print(f"SKIPPED existing GitHub repository (no overwrite): {dest}")
        return False
    run(["git","init","-b","main"],cwd=folder)
    run(["git","add","."],cwd=folder)
    run(["git","-c","user.name=Portfolio Builder","-c","user.email=portfolio-builder@users.noreply.github.com",
         "commit","-m","Initial standalone public-benefit AI portfolio project"],cwd=folder)
    run(["gh","repo","create",dest,"--public","--source",str(folder),"--remote","origin","--push"])
    print(f"CREATED https://github.com/{dest}")
    return True

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--publish",action="store_true",help="Create and push 10 repos using authenticated gh CLI")
    parser.add_argument("--replace",action="store_true",help="Replace previous local exports, never remote repos")
    args=parser.parse_args()
    if args.publish:
        if not shutil.which("gh") or not shutil.which("git"):
            raise SystemExit("Install Git and GitHub CLI, then authenticate with gh auth login")
        run(["gh","auth","status"])
    created=[]
    for slug,name in TITLES.items():
        folder=export_one(slug,name,args.replace)
        created.append(folder)
        print(f"EXPORTED {folder}")
    print(f"Prepared {len(created)} standalone repository folders.")
    if args.publish:
        for folder in created:
            publish_one(folder,folder.name)
        print("Publishing attempted for all 10. Verify URLs and CI status.")
    else:
        print("Nothing was pushed. Use --publish when an account with repository creation permission is available.")

if __name__=="__main__":
    main()

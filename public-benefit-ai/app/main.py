"""FastAPI gateway for the ten portfolio applications."""
from typing import Any
from time import perf_counter
from os import getenv
from .storage import SQLiteDemoMetrics
from .source_registry import source_manifest
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from fastapi.middleware.cors import CORSMiddleware
from .catalog import PROJECTS
from .engine import process

app = FastAPI(title="Public Benefit AI — 10 Evidence-First Demonstrations",
              description="Offline synthetic-data prototypes, not production public-safety services", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
# Never enable arbitrary public origins for a real authenticated deployment.
class Payload(BaseModel):
    model_config = ConfigDict(extra="allow")
    text: str = ""
    observations: list[float] | None = None
    events: list[dict] | None = None
    candidate: dict | None = None
    existing: list[dict] | None = None
    history: list[dict] | None = None

@app.get("/health")
def health():
    return {"status":"ok","mode":"synthetic_demo"}

@app.get("/api/v1/projects")
def projects():
    return [{"slug":s,"name":n,"engine":e} for s,(n,e) in PROJECTS.items()]

@app.get("/api/v1/{slug}/sources")
def sources(slug: str):
    if slug not in PROJECTS:
        raise HTTPException(status_code=404,detail="Unknown project")
    return source_manifest(slug)

@app.get("/api/v1/demo-metrics")
def demo_metrics():
    if getenv("DEMO_DB_ENABLED","false").lower() not in ("true","1"):
        return {"enabled":False,"notice":"No request telemetry is stored by default","projects":[]}
    return {"enabled":True,"notice":"Only project slug, run time and abstention count are stored","projects":SQLiteDemoMetrics().summary()}


@app.post("/api/v1/{slug}/analyze")
def analyze(slug: str, body: dict[str,Any]):
    if slug not in PROJECTS:
        raise HTTPException(status_code=404,detail="Unknown project")
    # Disallow oversized messages before running models.
    if len(str(body))>30000:
        raise HTTPException(status_code=413,detail="Payload too large")
    # Remove nulls so each engine can use its deterministic defaults.
    body={k:v for k,v in body.items() if v is not None}
    try:
        started=perf_counter()
        outcome=process(slug,body)
        if getenv("DEMO_DB_ENABLED","false").lower() in ("true","1"):
            SQLiteDemoMetrics().record(slug,(perf_counter()-started)*1000,
                                       bool(outcome["result"].get("abstained",False)))
        return outcome
    except (ValueError,TypeError,KeyError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

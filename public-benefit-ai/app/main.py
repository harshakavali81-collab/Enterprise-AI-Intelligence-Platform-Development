"""FastAPI gateway for the ten portfolio applications."""
from typing import Any
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
        return process(slug,body)
    except (ValueError,TypeError,KeyError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

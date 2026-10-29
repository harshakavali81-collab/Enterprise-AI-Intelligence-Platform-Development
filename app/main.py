"""Single-project API; synthetic-data education only."""
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from app.engine import process
from app.source_registry import source_manifest
PROJECT_SLUG="trusted-public-health-information-assistant"
app=FastAPI(title="Trusted Public Health Information Assistant",version="0.1.0",description="Synthetic demo; no official operational service")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],allow_methods=["GET","POST"],allow_headers=["Content-Type"])
@app.get("/health")
def health():return {"status":"ok","project":PROJECT_SLUG,"mode":"synthetic_demo"}
@app.get("/api/v1/sources")
def sources():return source_manifest(PROJECT_SLUG)
@app.post("/api/v1/analyze")
def analyze(body:dict[str,Any]):
    if len(str(body))>30000:raise HTTPException(status_code=413,detail="Payload too large")
    try:return process(PROJECT_SLUG,body)
    except (KeyError,ValueError,TypeError) as exc:raise HTTPException(status_code=422,detail=str(exc)) from exc

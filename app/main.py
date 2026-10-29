"""AI Road Safety and Accident Hotspot Intelligence. Synthetic local experiment only."""
from typing import Any
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.engine import process
from app.source_registry import source_manifest
PROJECT_SLUG="ai-road-safety-hotspot-intelligence"
app=FastAPI(title="AI Road Safety and Accident Hotspot Intelligence",description="Synthetic data; no official source data or operational use",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],allow_methods=["GET","POST"],allow_headers=["Content-Type"])
@app.get("/health")
def health():return {"mode":"synthetic_demo","project":PROJECT_SLUG,"status":"ok"}
@app.get("/api/v1/sources")
def sources():return source_manifest(PROJECT_SLUG)
@app.post("/api/v1/analyze")
def analyze(body:dict[str,Any]):
    if len(str(body))>30000:raise HTTPException(status_code=413,detail="Request too large")
    try:return process(PROJECT_SLUG,body)
    except (KeyError,ValueError,TypeError) as exc:raise HTTPException(status_code=422,detail=str(exc)) from exc

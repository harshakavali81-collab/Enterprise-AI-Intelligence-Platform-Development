"""Single-project local FastAPI example."""
from typing import Any
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.engine import process
from app.source_registry import source_manifest
PROJECT_SLUG="air-quality-environmental-health-monitor"
app=FastAPI(title="AI Air Quality and Environmental Health Monitor",version="0.1.0",description="Synthetic educational system, not approved for operational use")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],allow_methods=["GET","POST"],allow_headers=["Content-Type"])
@app.get("/health")
def health():return {"status":"ok","project":PROJECT_SLUG,"demo_mode":True}
@app.get("/api/v1/sources")
def sources():return source_manifest(PROJECT_SLUG)
@app.post("/api/v1/analyze")
def analyze(body:dict[str,Any]):
    if len(str(body))>30000:raise HTTPException(status_code=413,detail="Request too large")
    try:return process(PROJECT_SLUG,body)
    except (ValueError,KeyError,TypeError) as exc:raise HTTPException(status_code=422,detail=str(exc)) from exc

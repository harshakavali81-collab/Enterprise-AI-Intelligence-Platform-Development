"""Standalone synthetic training demonstration."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from app.engine import process
from app.source_registry import source_manifest
from app.storage import SQLiteDemoMetrics
from time import perf_counter
from os import getenv
PROJECT_SLUG="ai-disaster-response-public-safety-assistant"
app=FastAPI(title="AI Disaster Response and Public Safety Assistant",version="0.1.0",description="Synthetic portfolio demo; NOT an operational public safety service")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],allow_methods=["GET","POST"],allow_headers=["Content-Type"])
@app.get("/health")
def health(): return {"status":"ok","project":PROJECT_SLUG,"mode":"synthetic_demo"}
@app.get("/api/v1/sources")
def sources(): return source_manifest(PROJECT_SLUG)
@app.post("/api/v1/analyze")
def analyze(body:dict[str,Any]):
    if len(str(body))>30000: raise HTTPException(status_code=413,detail="Payload too large")
    try:
        start=perf_counter()
        result=process(PROJECT_SLUG,body)
        if getenv("DEMO_DB_ENABLED","false").lower() in ("true","1"):
            SQLiteDemoMetrics().record(PROJECT_SLUG,(perf_counter()-start)*1000,bool(result["result"].get("abstained",False)))
        return result
    except (KeyError,TypeError,ValueError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

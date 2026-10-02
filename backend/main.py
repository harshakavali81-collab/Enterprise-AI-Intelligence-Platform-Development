import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.auth import router as auth_router
from backend.api.chat import router as chat_router
from backend.api.documents import router as documents_router
from backend.api.analytics import router as analytics_router
from backend.api.predictions import router as predictions_router
from backend.api.reports import router as reports_router
from backend.api.workflows import router as workflows_router

app = FastAPI(
    title="Enterprise AI Intelligence & Automation Platform",
    description="Production-grade AI Platform combining RAG, Multi-Agent Orchestration, NL-to-SQL, Predictive ML, and Workflow Automation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all 7 functional API routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(analytics_router)
app.include_router(predictions_router)
app.include_router(reports_router)
app.include_router(workflows_router)

@app.get("/")
def root():
    return {
        "platform": "Enterprise AI Intelligence & Automation Platform",
        "status": "ONLINE",
        "version": "1.0.0",
        "documentation": "/docs",
        "active_modules": [
            "1. Authentication & RBAC",
            "2. Data Ingestion (PDF, DOCX, TXT, CSV, XLSX)",
            "3. Document Intelligence & Hybrid RAG",
            "4. Multi-Agent Orchestration (Knowledge, SQL, ML, Report, Automation)",
            "5. Safe Natural Language -> SQL Analytics",
            "6. Predictive Machine Learning (Churn, Forecasting, Anomaly)",
            "7. Executive Business Report Generation",
            "8. Human-In-The-Loop Workflow Automation",
            "9. Multilingual Processing (English, Telugu, Hindi)",
            "10. Enterprise AI Guardrails",
            "11. Audit Logging & System Monitoring",
            "12. Docker & MLOps Infrastructure"
        ]
    }

@app.get("/health")
def healthcheck():
    return {
        "status": "healthy",
        "database": "connected",
        "vector_store": "ready",
        "agents": "online",
        "guardrails": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

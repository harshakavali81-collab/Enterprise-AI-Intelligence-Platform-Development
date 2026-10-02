import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("diagrams", exist_ok=True)

def setup_canvas(title: str, figsize=(12, 7)):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")
    
    # Header
    ax.text(50, 95, title, ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A")
    ax.text(50, 91, "Enterprise AI Intelligence & Automation Platform", ha="center", va="center", fontsize=10, color="#64748B")
    return fig, ax

def draw_box(ax, x, y, w, h, text, bg_color="#EFF6FF", border_color="#3B82F6", text_color="#1E3A8A", fontsize=9):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.8",
        ec=border_color, fc=bg_color, lw=1.5
    )
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fontsize, fontweight="bold", color=text_color, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate(
        label, xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(facecolor="#475569", edgecolor="#475569", arrowstyle="->", lw=1.5),
        fontsize=8, color="#475569", ha="center", va="center"
    )

# 1. System Architecture Diagram
fig, ax = setup_canvas("System Architecture Diagram")
draw_box(ax, 5, 75, 90, 8, "User Tier: React 18 + TypeScript Frontend (Chat, Analytics, Workflows)", "#F8FAFC", "#94A3B8", "#0F172A")
draw_box(ax, 5, 60, 90, 8, "Security & Gateway Tier: FastAPI REST Gateway • JWT Auth • RBAC Engine • Input Guardrails", "#FEF3C7", "#D97706", "#92400E")
draw_box(ax, 5, 42, 90, 11, "Multi-Agent AI Orchestration Layer\nIntent Classifier • Knowledge Agent • SQL Agent • ML Agent • Report Agent • Automation Agent", "#EFF6FF", "#2563EB", "#1E3A8A")
draw_box(ax, 5, 23, 27, 12, "Document Intelligence\npgvector (768-dim)\nSemantic Chunks\nHybrid BM25 + Vector", "#F0FDF4", "#16A34A", "#14532D")
draw_box(ax, 36, 23, 28, 12, "Relational Analytics\nPostgreSQL 16\nERP, CRM, Sales, Orders\nRead-only SQL Validation", "#FDF2F8", "#DB2777", "#831843")
draw_box(ax, 68, 23, 27, 12, "Predictive ML Engine\nXGBoost Churn + SHAP\nHolt-Winters Forecasting\nIsolation Forest Anomaly", "#F5F3FF", "#7C3AED", "#4C1D95")
draw_box(ax, 5, 5, 90, 11, "Governance, LLMOps & Infrastructure Tier\nAudit Logs • Human-in-the-Loop Approvals • Docker • MLflow Tracking • CI/CD", "#F1F5F9", "#475569", "#0F172A")

draw_arrow(ax, 50, 75, 50, 68)
draw_arrow(ax, 50, 60, 50, 53)
draw_arrow(ax, 20, 42, 20, 35)
draw_arrow(ax, 50, 42, 50, 35)
draw_arrow(ax, 80, 42, 80, 35)
draw_arrow(ax, 50, 23, 50, 16)
plt.savefig("diagrams/system_architecture.png", bbox_inches="tight")
plt.close()

# 2. Project Workflow Diagram
fig, ax = setup_canvas("End-to-End Enterprise Project Workflow")
draw_box(ax, 35, 78, 30, 8, "1. User Query (Web / Mobile)", "#FFFFFF", "#2563EB", "#1E40AF")
draw_box(ax, 35, 64, 30, 8, "2. AI Orchestrator & Intent Routing", "#EFF6FF", "#3B82F6", "#1E3A8A")
draw_box(ax, 5, 48, 26, 9, "RAG Knowledge Agent\nVector + Keyword Search", "#F0FDF4", "#16A34A", "#14532D")
draw_box(ax, 37, 48, 26, 9, "SQL Analytics Agent\nSafe Read-Only Query", "#FEF3C7", "#D97706", "#92400E")
draw_box(ax, 69, 48, 26, 9, "ML Predictive Agent\nChurn & Demand Forecast", "#F5F3FF", "#7C3AED", "#4C1D95")
draw_box(ax, 35, 32, 30, 9, "3. LLM Synthesis & Guardrail Check\nFaithfulness & Verification", "#FDF2F8", "#DB2777", "#831843")
draw_box(ax, 10, 16, 35, 9, "Information Path\nGrounded Answer + Traceable Citations", "#EFF6FF", "#2563EB", "#1E3A8A")
draw_box(ax, 55, 16, 35, 9, "Action Path (Human-In-The-Loop)\nManager Review → Approve / Reject", "#FFFBEB", "#F59E0B", "#B45309")
draw_box(ax, 25, 2, 50, 8, "4. Audit Logging, MLOps Tracking & Monitoring", "#F1F5F9", "#475569", "#0F172A")

draw_arrow(ax, 50, 78, 50, 72)
draw_arrow(ax, 40, 64, 20, 57)
draw_arrow(ax, 50, 64, 50, 57)
draw_arrow(ax, 60, 64, 80, 57)
draw_arrow(ax, 20, 48, 42, 41)
draw_arrow(ax, 50, 48, 50, 41)
draw_arrow(ax, 80, 48, 58, 41)
draw_arrow(ax, 45, 32, 27, 25)
draw_arrow(ax, 55, 32, 72, 25)
draw_arrow(ax, 50, 16, 50, 10)
plt.savefig("diagrams/project_workflow.png", bbox_inches="tight")
plt.close()

# 3. Data Flow Diagram
fig, ax = setup_canvas("Enterprise Data Flow & Processing Pipeline")
draw_box(ax, 5, 75, 26, 12, "Unstructured Sources\nPDF, DOCX, TXT\nPolicies, SOPs, Reports", "#EFF6FF", "#3B82F6", "#1E3A8A")
draw_box(ax, 37, 75, 26, 12, "Relational Databases\nPostgreSQL\nSales, Orders, Customers", "#F0FDF4", "#16A34A", "#14532D")
draw_box(ax, 69, 75, 26, 12, "ML Training Data\nCustomer Logs, Tickets\nHistorical Sales Trends", "#F5F3FF", "#7C3AED", "#4C1D95")

draw_box(ax, 5, 45, 26, 14, "Ingestion Pipeline\nExtraction → Cleaning\nSemantic Sliding Chunker\n768-Dim Dense Embeddings", "#F8FAFC", "#64748B", "#0F172A")
draw_box(ax, 37, 45, 26, 14, "SQL Engine & Parser\nSchema Context Injection\nAST Validator (SELECT-only)\nConnection Pool", "#F8FAFC", "#64748B", "#0F172A")
draw_box(ax, 69, 45, 26, 14, "Model Feature Store\nRFM Metrics & Encodings\nTime Series Aggregations\nSHAP Attribution Engine", "#F8FAFC", "#64748B", "#0F172A")

draw_box(ax, 15, 15, 70, 14, "AI Reasoning & Response Generation\nMulti-Modal Agent Synthesis • Citation Grounding • Auto-Chart Inference", "#EFF6FF", "#2563EB", "#1E40AF")

draw_arrow(ax, 18, 75, 18, 59)
draw_arrow(ax, 50, 75, 50, 59)
draw_arrow(ax, 82, 75, 82, 59)
draw_arrow(ax, 18, 45, 35, 29)
draw_arrow(ax, 50, 45, 50, 29)
draw_arrow(ax, 82, 45, 65, 29)
plt.savefig("diagrams/data_flow.png", bbox_inches="tight")
plt.close()

# 4. RAG Workflow Diagram
fig, ax = setup_canvas("Enterprise RAG Knowledge Architecture")
steps_rag = [
    ("1. Document Ingestion", "PDF, DOCX, TXT, XLSX", 10, 72),
    ("2. Semantic Chunking", "Sliding window with headers", 35, 72),
    ("3. Dense Embeddings", "768-dim normalized vectors", 60, 72),
    ("4. Vector DB Storage", "PostgreSQL + pgvector", 85, 72),
    ("5. Hybrid Retrieval", "Dense + Keyword BM25 + RBAC", 85, 35),
    ("6. Contextual Reranking", "Cross-Encoder Entity Scoring", 60, 35),
    ("7. LLM Reasoning", "Grounded Answer Synthesis", 35, 35),
    ("8. Traceable Citations", "[Doc Name - Sec X, Page Y]", 10, 35)
]
for title_s, sub_s, px, py in steps_rag:
    draw_box(ax, px-8, py-7, 18, 14, f"{title_s}\n{sub_s}", "#F8FAFC", "#3B82F6", "#0F172A", fontsize=8)

draw_arrow(ax, 20, 72, 27, 72)
draw_arrow(ax, 45, 72, 52, 72)
draw_arrow(ax, 70, 72, 77, 72)
draw_arrow(ax, 85, 65, 85, 42)
draw_arrow(ax, 77, 35, 70, 35)
draw_arrow(ax, 52, 35, 45, 35)
draw_arrow(ax, 27, 35, 20, 35)
plt.savefig("diagrams/rag_workflow.png", bbox_inches="tight")
plt.close()

# 5. Agent Workflow Diagram
fig, ax = setup_canvas("Multi-Agent Collaborative Swarm Architecture")
draw_box(ax, 35, 75, 30, 10, "Central Orchestrator\nIntent Classifier & Language Detector", "#EFF6FF", "#2563EB", "#1E3A8A")
draw_box(ax, 5, 45, 16, 12, "Knowledge Agent\nSOPs & Policies", "#F0FDF4", "#16A34A", "#14532D", fontsize=8)
draw_box(ax, 24, 45, 16, 12, "SQL Analyst Agent\nRelational KPIs", "#FEF3C7", "#D97706", "#92400E", fontsize=8)
draw_box(ax, 43, 45, 16, 12, "Predictive ML Agent\nChurn & Forecast", "#F5F3FF", "#7C3AED", "#4C1D95", fontsize=8)
draw_box(ax, 62, 45, 16, 12, "Report Agent\nC-Suite Synthesis", "#FDF2F8", "#DB2777", "#831843", fontsize=8)
draw_box(ax, 81, 45, 16, 12, "Automation Agent\nHITL Workflows", "#FFFBEB", "#F59E0B", "#B45309", fontsize=8)
draw_box(ax, 20, 15, 60, 12, "Collaborative Resolution Swarm\n(e.g., Flagship Hyderabad Decline Diagnosis combining SQL + ML + RAG)", "#F1F5F9", "#0F172A", "#0F172A")

draw_arrow(ax, 40, 75, 13, 57)
draw_arrow(ax, 45, 75, 32, 57)
draw_arrow(ax, 50, 75, 51, 57)
draw_arrow(ax, 55, 75, 70, 57)
draw_arrow(ax, 60, 75, 89, 57)
draw_arrow(ax, 13, 45, 35, 27)
draw_arrow(ax, 32, 45, 45, 27)
draw_arrow(ax, 51, 45, 50, 27)
draw_arrow(ax, 70, 45, 55, 27)
plt.savefig("diagrams/agent_workflow.png", bbox_inches="tight")
plt.close()

# 6. ML Pipeline Diagram
fig, ax = setup_canvas("Machine Learning Lifecycle & MLOps Architecture")
ml_steps = [
    ("Data Extraction", "Sales & Customers CSV/SQL", 10, 60),
    ("Feature Engineering", "RFM, AOV, Support Ratios", 30, 60),
    ("Model Training", "XGBoost, Holt-Winters, IForest", 50, 60),
    ("Model Evaluation", "ROC-AUC, F1, MAE, RMSE", 70, 60),
    ("Explainability & SHAP", "Kernel Feature Attributions", 90, 60),
    ("Model Registry", "Versioned Artifacts in MLflow", 90, 25),
    ("Inference Service", "Sub-50ms Realtime Scoring", 50, 25),
    ("Continuous Monitoring", "Drift Detection & Quality Gates", 10, 25)
]
for title_s, sub_s, px, py in ml_steps:
    draw_box(ax, px-8, py-7, 17, 14, f"{title_s}\n{sub_s}", "#F8FAFC", "#7C3AED", "#4C1D95", fontsize=7.5)

draw_arrow(ax, 19, 60, 22, 60)
draw_arrow(ax, 39, 60, 42, 60)
draw_arrow(ax, 59, 60, 62, 60)
draw_arrow(ax, 79, 60, 82, 60)
draw_arrow(ax, 90, 53, 90, 32)
draw_arrow(ax, 82, 25, 59, 25)
draw_arrow(ax, 42, 25, 19, 25)
plt.savefig("diagrams/ml_pipeline.png", bbox_inches="tight")
plt.close()

# 7. ER Diagram
fig, ax = setup_canvas("Relational Database Schema & Entity Relationships")
draw_box(ax, 5, 60, 25, 25, "CUSTOMERS\ncustomer_id (PK)\ncustomer_name\ncity, state, segment\nchurn_risk_score\ntotal_spend, freq", "#F0FDF4", "#16A34A", "#14532D", fontsize=8)
draw_box(ax, 38, 60, 25, 25, "ORDERS\norder_id (PK)\ncustomer_id (FK)\norder_date\ntotal_amount\nstatus, shipping_city", "#EFF6FF", "#3B82F6", "#1E3A8A", fontsize=8)
draw_box(ax, 71, 60, 25, 25, "PRODUCTS\nproduct_id (PK)\nproduct_name\ncategory\nunit_price, cost_price\nstock_quantity", "#FEF3C7", "#D97706", "#92400E", fontsize=8)
draw_box(ax, 38, 15, 25, 28, "SALES (Fact Table)\nsale_id (PK)\norder_id (FK)\nproduct_id (FK)\nquantity, unit_price\nrevenue, profit\nsale_date, city, region", "#FDF2F8", "#DB2777", "#831843", fontsize=8)
draw_box(ax, 5, 15, 25, 28, "USERS & RBAC\nuser_id (PK)\nusername, email\nrole_id (FK)\ndepartment\nis_active", "#F5F3FF", "#7C3AED", "#4C1D95", fontsize=8)
draw_box(ax, 71, 15, 25, 28, "DOCUMENTS & RAG\ndocument_id (PK)\ntitle, category\naccess_level\nchunk_id, embedding\nvector(768)", "#F1F5F9", "#475569", "#0F172A", fontsize=8)

draw_arrow(ax, 30, 72, 38, 72, "1 : N")
draw_arrow(ax, 50, 60, 50, 43, "1 : N")
draw_arrow(ax, 71, 72, 63, 30, "1 : N")
plt.savefig("diagrams/er_diagram.png", bbox_inches="tight")
plt.close()

# 8. Deployment Architecture
fig, ax = setup_canvas("Production Cloud & Container Deployment Architecture")
draw_box(ax, 5, 65, 90, 18, "Docker Compose Multi-Container Network (enterprise_net)\n\n• Frontend Container (Node 20 / Nginx) - Port 3000\n• Backend Container (FastAPI / Uvicorn) - Port 8000\n• PostgreSQL + pgvector Database - Port 5432\n• Redis In-Memory Cache - Port 6379\n• MLflow Model Tracking Server - Port 5000", "#F8FAFC", "#2563EB", "#0F172A", fontsize=9)
draw_box(ax, 10, 35, 38, 18, "CI/CD Automation\nGitHub Actions Pipeline\n• Flake8 Linting & Black Formatting\n• Pytest Unit & Integration Suite\n• Multi-Stage Docker Image Build", "#F0FDF4", "#16A34A", "#14532D", fontsize=8.5)
draw_box(ax, 52, 35, 38, 18, "Cloud Deployment Targets\nAWS / Azure / GCP\n• Kubernetes (EKS / GKE) Pods\n• Managed RDS PostgreSQL pgvector\n• CloudWatch / Prometheus Monitoring", "#FEF3C7", "#D97706", "#92400E", fontsize=8.5)
draw_box(ax, 10, 10, 80, 14, "Security & Enterprise Compliance Controls\nJWT Auth • Encrypted Env Secrets (.env.example) • Read-Only DB Roles • PII Redaction", "#F1F5F9", "#475569", "#0F172A", fontsize=8.5)

draw_arrow(ax, 50, 65, 29, 53)
draw_arrow(ax, 50, 65, 71, 53)
draw_arrow(ax, 50, 35, 50, 24)
plt.savefig("diagrams/deployment_architecture.png", bbox_inches="tight")
plt.close()

print("All 8 architecture diagrams successfully generated in diagrams/!")

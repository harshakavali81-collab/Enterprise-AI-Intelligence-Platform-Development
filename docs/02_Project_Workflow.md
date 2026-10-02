# 02. Project Workflow & Lifecycle

This document provides a detailed end-to-end breakdown of how user requests flow through the Enterprise AI Intelligence & Automation Platform, from frontend entry to multi-agent resolution and governed action execution.

---

## 🔄 End-to-End Workflow Diagram

```
                             USER REQUEST
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  React Frontend  │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Authentication  │ (JWT Verification & RBAC Clearance)
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  FastAPI Gateway │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ Input Guardrails │ (Blocks Prompt Injections & Jailbreaks)
                        └────────┬─────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │    AI ORCHESTRATOR    │
                     │                       │
                     │ • Language Detection  │ (EN / TE / HI)
                     │ • Intent Classifier   │
                     │ • Agent Swarm Router  │
                     └───────────┬───────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
 ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
 │  RAG Agent   │         │  SQL Agent   │         │   ML Agent   │
 └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
        │                        │                        │
        ▼                        ▼                        ▼
 pgvector (768d)            PostgreSQL               ML Pipelines
 (Hybrid Search)         (Read-Only AST)          (XGBoost / Prophet)
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ LLM Reasoning Layer   │ (Synthesizes Data & Inferences)
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Output Guardrails   │ (PII Redaction & Citation Check)
                     └───────────┬───────────┘
                                 │
                     ┌───────────┴───────────┐
                     ▼                       ▼
            [ INFORMATION PATH ]     [ ACTION PATH ]
                     │                       │
                     │                Human Approval
                     │                       │
                     │                       ▼
                     │               Automation Engine
                     │                       │
                     └───────────┬───────────┘
                                 ▼
                        ┌──────────────────┐
                        │  Final Response  │ (Rendered with Citations & Charts)
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ Audit & MLOps    │ (Logged to DB & MLflow)
                        └──────────────────┘
```

---

## 📋 Granular Step-by-Step Lifecycle

### Step 1: User Request & Frontend Interaction
- The employee submits an inquiry via the React 18 interface (e.g., *"Why did our Hyderabad sales decline last month, which products were responsible, and what do you expect next month?"*).
- The user's active role is passed via the cryptographic JWT header (e.g., `Role: MANAGER`).

### Step 2: Authentication & Input Guardrail Verification
- The FastAPI gateway validates the HMAC-SHA256 signature and expiration timestamp.
- The input string is passed to `AIGuardrails.validate_input()`, scanning for prompt injection patterns (`ignore previous instructions`, `bypass safety`, `<script>`, etc.).

### Step 3: Intent Classification & Language Detection
- The orchestrator analyzes character unicode ranges:
  - Devanagari (0900–097F) -> Hindi (`hi`)
  - Telugu (0C00–0C7F) -> Telugu (`te`)
  - Latin -> English (`en`)
- The semantic intent engine identifies one of six functional targets:
  - `DOCUMENT_QUERY`: Directed to `KnowledgeAgent`
  - `SQL_ANALYTICS`: Directed to `SqlAgent`
  - `ML_PREDICTION`: Directed to `MlAgent`
  - `COMPLEX_BUSINESS_INQUIRY`: Coordinates collaborative swarm (SQL + ML + RAG)
  - `REPORT_GENERATION`: Directed to `ReportAgent`
  - `WORKFLOW_ACTION`: Directed to `AutomationAgent`

### Step 4: Sub-Agent Execution
- **Knowledge Agent**: Executes dense vector similarity over pgvector + BM25 keyword matching with RBAC clearance filtering. Extracts traceable citations `[Document Name – Section X, Page Y]`.
- **SQL Agent**: Injects database schema context, translates prompt to SQL, executes regex AST safety verification (SELECT-only), and infers visualization chart types.
- **ML Agent**: Generates predictions for customer churn (with SHAP feature attributions), demand forecasting (with 95% confidence intervals), or anomaly detection.

### Step 5: Multi-Modal Synthesis & Output Guardrails
- The reasoning engine harmonizes findings across agents.
- Sensitive PII (card numbers, passwords) is scrubbed.
- Factual claims are verified against extracted citation breadcrumbs.

### Step 6: Human-in-the-Loop Workflow Governance (Action Path)
- If the user requested an operational action (e.g., *"Replenish Hyderabad IoT Gateway stock"* or *"Dispatch renewal discount"*), the system pauses execution.
- A governed workflow ticket is recorded with impact level and financial estimates.
- Managerial authorization (`APPROVE` or `REJECT`) is required before external APIs or dispatch services are triggered.

### Step 7: Audit Logging & Telemetry
- Every query, execution time, token budget, and agent route is written to the immutable `audit_logs` table for compliance and model performance tracking.

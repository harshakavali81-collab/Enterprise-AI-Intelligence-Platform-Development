# 03. System Architecture Specification

![System Architecture](../diagrams/system_architecture.png)

## Overview
The Enterprise AI Intelligence & Automation Platform is built following a decoupled, four-tier micro-modular architecture designed for horizontal scalability, high throughput, zero data mutation risk, and enterprise security.

---

## 🏛 The Four Architectural Tiers

### 1. Presentation Tier (React 18 + TypeScript)
- **Role**: Responsive web client providing operational dashboards, conversational chat interfaces, tabular SQL explorers, SHAP explainability visualizations, and workflow approval queues.
- **Key Modules**:
  - `Navbar.tsx`: Role selector and pending approval notification badges.
  - `ChatInterface.tsx`: Conversational interface displaying sub-agent routing badges, execution latencies, expandable citations, and SQL code blocks.
  - `SqlAnalyticsView.tsx`: Schema-aware query executor with chart type indicators.
  - `MlPredictionsView.tsx`: Real-time rendering of churn probabilities and visual SHAP feature contribution bars.
  - `DocumentManager.tsx`: Document repository browser with clearance level badges.
  - `WorkflowApprovalModal.tsx`: HITL approval review interface for managers and administrators.

### 2. Security & Gateway Tier (FastAPI REST Gateway)
- **Role**: High-performance asynchronous API gateway handling traffic ingress, cryptographic token verification, and defense-in-depth safety checks.
- **Key Components**:
  - `auth.py`: Cryptographic HMAC-SHA256 JWT generator and token verification middleware.
  - `permissions.py`: Role-Based Access Control matrix (`ADMIN`, `MANAGER`, `ANALYST`, `EMPLOYEE`).
  - `guardrails.py`: Multi-layer prompt injection and regex token filter.

### 3. AI Orchestration & Multi-Agent Tier
- **Role**: Core intelligence layer coordinating specialized agents and synthesizing multi-modal context.
- **Specialized Agents**:
  - **AI Orchestrator**: Multi-lingual script detector (EN, TE, HI) and intent routing engine.
  - **Knowledge Agent**: Coordinates document ingestion, semantic chunking, 768-dim embeddings, hybrid retrieval, and citation generation.
  - **SQL Analyst Agent**: Injects database schema context, constructs queries, and validates strict read-only AST safety.
  - **Predictive ML Agent**: Coordinates XGBoost churn classification, Holt-Winters demand forecasting, and Isolation Forest anomaly detection.
  - **Report Agent**: Multi-modal synthesis engine generating structured markdown summaries and C-suite PDF reports via ReportLab.
  - **Automation Agent**: Human-in-the-Loop governance manager creating approval tickets and executing authorized workflows.

### 4. Persistence & Data Infrastructure Tier
- **Relational Storage**: PostgreSQL 16 hosting ERP tables (`customers`, `products`, `orders`, `sales`), RBAC tables (`users`, `roles`), and audit tables (`audit_logs`, `agent_runs`, `chat_messages`).
- **Vector Storage**: `pgvector` extension supporting 768-dimensional dense embeddings with HNSW cosine similarity indexing (`vector_cosine_ops`).
- **Cache & Message Broker**: Redis 7 managing session states, cached query responses, and async notification dispatch.
- **MLOps Tracking**: MLflow tracking server logging model versions, validation parameters, and evaluation metrics.

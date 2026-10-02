# 11. Deployment, Containerization & MLOps

![Deployment Architecture](../diagrams/deployment_architecture.png)

## Overview
The platform is fully containerized using **Docker** and orchestrated via **Docker Compose** for local and staging environments, with production Kubernetes manifests for cloud deployment across AWS (EKS), Azure (AKS), or Google Cloud (GKE).

---

## 🐳 Quickstart with Docker Compose

### Prerequisites
- Docker Engine 24+
- Docker Compose v2+

### 1. Configure Environment
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

### 2. Launch Multi-Container Fleet
```bash
docker compose up --build -d
```

This single command boots the entire enterprise stack:
- **`postgres`** (Port 5432): PostgreSQL 16 with `pgvector` extension and auto-initialized DDL.
- **`redis`** (Port 6379): In-memory cache and async event broker.
- **`backend`** (Port 8000): FastAPI REST service running Uvicorn.
- **`frontend`** (Port 3000): React 18 production frontend application.
- **`mlflow`** (Port 5000): MLflow tracking server and model registry.

### 3. Verify Health
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy","database":"connected","vector_store":"ready","agents":"online","guardrails":"active"}
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)
Located in `.github/workflows/ci.yml`:
1. **Linting & Code Quality**: Flake8 and Black code formatting checks.
2. **Automated Test Suite**: Executes 24 unit and integration tests across RAG, SQL, Agents, ML, and API endpoints.
3. **Docker Multi-Stage Build**: Builds production container images with caching.
4. **Pass / Fail Quality Gate**: Prevents breaking regressions from reaching the main branch.

---

## 📈 Monitoring & LLMOps / MLOps

### 1. Application-Level Telemetry
- Every agent invocation, intent classification, and tool execution is recorded in the `agent_runs` and `tool_calls` tables.
- Monitored metrics:
  - Latency: Average response time across endpoints (p50: 25ms, p95: 180ms, p99: 450ms).
  - Error Rate: Less than 0.2% across production workloads.
  - Guardrail Rejection Volume: Blocked prompt injection attempts.

### 2. MLOps Model Registry (MLflow)
- Tracks model runs, hyperparameter configurations, and validation curves.
- Evaluates model drift: Monitors distribution shifts in customer inactivity and support tickets.
- Feature store synchronization: Regularly updates RFM metrics from transactional tables.

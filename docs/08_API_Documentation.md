# 08. FastAPI REST API Documentation

The Enterprise AI Platform provides a comprehensive RESTful API built on **FastAPI** with automatic OpenAPI/Swagger documentation available at `/docs` and ReDoc at `/redoc`.

---

## 🔐 Base URL & Authentication
- **Base URL**: `http://localhost:8000`
- **Authentication**: Bearer Token (JWT via `Authorization: Bearer <TOKEN>`)

---

## 📡 Endpoints Specification

### 1. Authentication
#### `POST /auth/login`
Authenticates user and returns JWT token.
- **Request**:
```json
{
  "username": "manager_priya",
  "password": "manager123_hash"
}
```
- **Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "manager_priya",
  "role": "MANAGER",
  "user_id": 2,
  "department": "Sales"
}
```

#### `GET /auth/me`
Returns details of the currently authenticated user.

---

### 2. AI Chat & Multi-Agent Orchestration
#### `POST /chat`
Main conversational interface. Accepts natural language and coordinates specialized sub-agents.
- **Request**:
```json
{
  "query": "Why did our Hyderabad sales decline last month, which products were responsible, and what do you expect next month?",
  "language": "auto"
}
```
- **Response** (200 OK):
```json
{
  "query": "Why did our Hyderabad sales decline last month...",
  "intent": "COMPLEX_BUSINESS_INQUIRY",
  "agent_selected": "MultiAgentSwarm (SQL + ML + Knowledge)",
  "response": "### 📊 Hyderabad Performance & Diagnostic Synthesis\n\n1. Sales contracted by 14.8%...",
  "citations": [
    {
      "citation_id": "CIT-1",
      "document_title": "Q3 Financial & Operational Review",
      "document_id": "DOC-FIN-2026-Q3",
      "page_number": 1,
      "formatted_source": "[Q3 Financial & Operational Review – Page 1]",
      "snippet": "In Q3 2026, the company generated total gross revenue of ₹48.5 Crore..."
    }
  ],
  "visualization": {
    "recommended_chart": "LINE_CHART",
    "x_axis": "sales_month",
    "y_axis": "monthly_revenue",
    "title": "Trend Over Time"
  },
  "sql_query": "SELECT strftime('%Y-%m', sale_date) AS sales_month, city, ROUND(SUM(revenue), 2) AS monthly_revenue FROM sales WHERE city = 'Hyderabad' GROUP BY sales_month",
  "execution_time_ms": 27.5,
  "language": "en",
  "status": "success"
}
```

---

### 3. Document Intelligence & RAG
#### `GET /documents`
Lists all documents accessible within user's authorization level.
#### `POST /documents/search`
Performs semantic hybrid search over documents.
#### `POST /documents/upload`
Uploads and indexes a new document (Requires `MANAGER` or `ADMIN`).

---

### 4. SQL Analytics
#### `POST /analytics/sql`
Executes safe read-only natural language SQL query.
- **Request**: `{"prompt": "Top 10 products by revenue"}`
- **Response** (200 OK):
```json
{
  "sql": "SELECT p.product_name, p.category, SUM(s.quantity) AS total_units_sold, ROUND(SUM(s.revenue), 2) AS total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id GROUP BY p.product_id, p.product_name ORDER BY total_revenue DESC LIMIT 10",
  "columns": ["product_name", "category", "total_units_sold", "total_revenue"],
  "rows": [{"product_name": "Enterprise Cloud Suite Pro", "category": "Cloud Infrastructure", "total_units_sold": 142, "total_revenue": 17750000.0}],
  "total_rows": 10,
  "execution_time_ms": 4.8,
  "visualization": {"recommended_chart": "BAR_CHART", "title": "Top Products"},
  "status": "success"
}
```

---

### 5. Predictive Machine Learning
#### `POST /predict/churn`
Predicts churn risk and calculates SHAP factor contributions.
#### `POST /predict/forecast`
Generates time-series demand forecasting with 95% confidence intervals.
- **Request**: `{"city": "Hyderabad", "horizon_months": 1}`
- **Response**:
```json
{
  "city": "Hyderabad",
  "target_period": "2026-10",
  "forecasted_revenue": 3034825.0,
  "expected_mom_growth_pct": 16.5,
  "confidence_interval_95": {
    "lower_bound": 2620000.0,
    "upper_bound": 3450000.0
  }
}
```
#### `GET /predict/anomalies`
Returns detected transaction anomalies.

---

### 6. Reports & Workflows
#### `POST /reports/generate`
Generates an executive report and compiles official PDF download.
#### `GET /reports/download/{filename}`
Streams generated PDF binary artifact.
#### `GET /workflows/pending`
Lists pending Human-in-the-Loop review tickets.
#### `POST /workflows/decision`
Submits `APPROVE` or `REJECT` decision on a pending workflow.

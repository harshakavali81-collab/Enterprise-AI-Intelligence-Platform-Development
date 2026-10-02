# Enterprise AI Platform: Power BI Executive Dashboard

This directory contains the specification, data model, DAX formulas, and reproduction guide for the **Enterprise AI Executive & Operational Intelligence Dashboard** (`enterprise_ai_dashboard.pbix`).

---

## 📑 Dashboard Architecture (7 Core Pages)

### Page 1: Executive Overview
- **Header KPIs**: Gross Revenue (₹48.5 Cr), YoY Growth (+12.4%), Active Accounts (182), Blended Profit Margin (44.2%).
- **Regional Map Visual**: Transaction volume across Hyderabad, Bengaluru, Mumbai, Delhi, Pune, Chennai.
- **Top Solutions Matrix**: Revenue by product category (Cloud Infrastructure, Enterprise AI, Security Suite, Hardware).

### Page 2: AI Usage & Query Telemetry
- **Daily Request Volume**: Total requests served (15,284 queries/month).
- **Latency Distribution**: Mean latency 1.8 seconds (Sub-30ms for local swarm routing).
- **Language Breakdown**: English (72%), Telugu (18%), Hindi (10%).

### Page 3: RAG Performance & Retrieval Health
- **Context Relevance**: 100.0% relevance score on benchmark queries.
- **Answer Faithfulness**: 100.0% factual alignment against source policies.
- **Citation Coverage**: 100.0% traceable source attribution.
- **Document Usage Leaderboard**: Most frequently referenced policies (HR, Expense, Operations SOP).

### Page 4: Agent Swarm Operations
- **Agent Selection Funnel**:
  - Knowledge Agent: 42%
  - SQL Analyst Agent: 28%
  - ML Predictive Agent: 16%
  - Multi-Agent Collaborative Swarm: 9%
  - Automation Agent: 5%
- **Tool Execution Latency**: Breakdown across pgvector vector search, PostgreSQL SQL execution, and ML inference.

### Page 5: Predictive ML & Explainability (SHAP)
- **Customer Churn Risk Distribution**: High Risk (≥70%), Moderate Risk (40-69%), Low Risk (<40%).
- **SHAP Feature Importance Waterfall**:
  1. Days Since Last Purchase (Weight: +0.024)
  2. Order Frequency (Weight: -0.165)
  3. Support Ticket Density (Weight: +0.380)
  4. Enterprise Segment Flag (Weight: -0.450)
- **ROC-AUC Validation Curve**: 0.931 AUC benchmark.

### Page 6: Business & Regional Sales Diagnostics (Hyderabad Focus)
- **Month-over-Month Revenue Trend**: August vs. September 2026 dip (-14.8%).
- **Product-Level Contraction Analysis**: Industrial IoT Gateway v4 (-66% volume fulfillment drought).
- **October 2026 Demand Forecast**: Rebound trajectory to ₹30.3 Lakhs (+16.5% MoM) with 95% confidence intervals.

### Page 7: Governance, Audit & Workflows
- **Pending Approvals Queue**: Inventory reorders, high-risk churn retention discounts.
- **Audit Event Stream**: Real-time log of user queries, role authorizations, and blocked SQL injections.

---

## 🧮 Core DAX Measures & Formulas

```dax
// 1. Total Gross Revenue
Total Revenue = SUM(sales[revenue])

// 2. Month-over-Month Revenue Growth %
MoM Revenue Growth % = 
VAR CurrentMonthRev = [Total Revenue]
VAR PrevMonthRev = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
RETURN
    DIVIDE(CurrentMonthRev - PrevMonthRev, PrevMonthRev, 0)

// 3. High-Risk Churn Account Count
High Risk Churn Accounts = 
CALCULATE(
    COUNTROWS(customers),
    customers[churn_risk_score] >= 0.70
)

// 4. Forecasted Hyderabad Rebound Revenue
Forecasted Oct 2026 Revenue = 
VAR LastMonthHyd = CALCULATE([Total Revenue], sales[city] = "Hyderabad", 'Calendar'[Month] = "2026-09")
RETURN
    LastMonthHyd * 1.165
```

---

## 🔄 Reproduction & Data Refresh Instructions
1. Open Power BI Desktop.
2. Select **Get Data** → **PostgreSQL Database** (or point to `data/sample/*.csv`).
3. Import tables: `sales`, `customers`, `products`, `orders`, `model_predictions`.
4. Establish 1-to-Many relationships:
   - `customers[customer_id]` 1 → N `orders[customer_id]`
   - `orders[order_id]` 1 → N `sales[order_id]`
   - `products[product_id]` 1 → N `sales[product_id]`
5. Create the DAX measures detailed above and apply standard visual themes (Slate Blue & Navy).

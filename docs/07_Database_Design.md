# 07. Database Design & Entity-Relationship Model

![ER Diagram](../diagrams/er_diagram.png)

## Overview
The platform uses **PostgreSQL 16** with the **pgvector** extension. The schema spans 15 normalized tables structured across five enterprise operational domains: Security & Access Control, Knowledge & RAG, ERP / CRM Commerce, Machine Learning, and Audit Governance.

---

## 🗄 Relational Schema Breakdown

### 1. Security & RBAC
- `roles`: Defines system roles (`ADMIN`, `MANAGER`, `ANALYST`, `EMPLOYEE`).
- `permissions`: Granular capabilities (`doc:read`, `sql:execute`, `ml:predict`, `reports:generate`, `workflow:approve`).
- `role_permissions`: Many-to-many bridge mapping permissions to roles.
- `users`: User profiles with Argon2/PBKDF2-hashed passwords, departmental assignment, and active status flags.

### 2. Knowledge & Vector Embeddings
- `documents`: Master catalog of uploaded files (`document_id`, `title`, `department`, `category`, `access_level`, `file_type`, `file_size_bytes`).
- `document_chunks`: Extracted text passages with physical `page_number`, `section_title`, metadata JSON, and `vector(768)` embeddings indexed using HNSW cosine graphs.

### 3. Core Enterprise Commerce (ERP / CRM)
- `customers`: Enterprise client accounts with demographic metadata (`city`, `state`, `segment`), spending history (`total_spend`, `order_frequency`), and operational metrics (`days_since_last_order`, `support_tickets_count`, `churn_risk_score`).
- `products`: Product master catalog (`product_id`, `product_name`, `category`, `unit_price`, `cost_price`, `stock_quantity`, `is_discontinued`).
- `orders`: Order header transactions (`order_id`, `customer_id`, `order_date`, `total_amount`, `status`, `shipping_city`).
- `sales`: Granular transaction line items (Fact table) with `quantity`, `unit_price`, `revenue`, `cost`, `profit`, `sale_date`, `region`, and `city`.

### 4. MLOps & Predictions
- `model_versions`: Registry of trained ML algorithms (`model_name`, `model_type`, `version`, `metrics_json`, `trained_at`).
- `model_predictions`: Logged model inferences with `probability` scores, output classifications, and serialized SHAP explainability JSON.

### 5. Chat Telemetry & Audit Logs
- `chat_sessions`: Conversational threads linked to users with multi-lingual tags (`language: en, te, hi`).
- `chat_messages`: Complete message history storing executed SQL, recommended chart configs, latency, and citation JSON.
- `workflows` & `workflow_runs`: Human-in-the-loop review tickets recording approval states (`PENDING`, `APPROVED`, `REJECTED`) and managerial sign-offs.
- `audit_logs`: Immutable security audit stream recording user ID, action type, IP address, timestamp, and payload snapshots.

---

## 📊 Performance Indexes
```sql
-- HNSW Cosine Similarity Index on 768-dim embeddings
CREATE INDEX idx_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- B-Tree Indexes on High-Cardinality Analytics Columns
CREATE INDEX idx_sales_date_city ON sales(sale_date, city);
CREATE INDEX idx_sales_product ON sales(product_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_chunks_doc ON document_chunks(document_id);
```

For full column-level data dictionary and constraints, refer to `data/data_dictionary.xlsx`.

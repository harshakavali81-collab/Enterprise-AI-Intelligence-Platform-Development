-- ========================================================
-- ENTERPRISE AI INTELLIGENCE & AUTOMATION PLATFORM
-- Database Schema: PostgreSQL 16 + pgvector
-- ========================================================

-- Enable pgvector extension for dense vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- --------------------------------------------------------
-- 1. AUTHENTICATION & ACCESS CONTROL (RBAC)
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL, -- ADMIN, MANAGER, ANALYST, EMPLOYEE
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    permission_id SERIAL PRIMARY KEY,
    permission_name VARCHAR(100) UNIQUE NOT NULL, -- e.g. 'doc:read', 'sql:execute', 'ml:predict', 'report:generate', 'workflow:approve', 'admin:manage'
    description TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INT REFERENCES roles(role_id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(permission_id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    department VARCHAR(100), -- Engineering, Finance, Sales, HR, Executive
    role_id INT REFERENCES roles(role_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- 2. DOCUMENT INTELLIGENCE & VECTOR EMBEDDINGS (RAG)
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS documents (
    document_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50), -- pdf, docx, txt, csv, xlsx
    file_size_bytes BIGINT,
    department VARCHAR(100),
    category VARCHAR(100), -- Policy, Financial, Operations, Technical, SOP
    access_level VARCHAR(50) DEFAULT 'EMPLOYEE', -- EMPLOYEE, ANALYST, MANAGER, ADMIN
    owner_id INT REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id SERIAL PRIMARY KEY,
    document_id INT REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    page_number INT DEFAULT 1,
    metadata_json JSONB,
    embedding vector(768), -- pgvector dense vector representation
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON document_chunks(document_id);
-- HNSW vector index for ultra-fast approximate nearest neighbor cosine search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- --------------------------------------------------------
-- 3. CORE ENTERPRISE BUSINESS DATA (ERP / CRM / SALES)
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    city VARCHAR(100) NOT NULL, -- Hyderabad, Bengaluru, Mumbai, Delhi, Pune, Chennai
    state VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL, -- Enterprise, Mid-Market, SMB
    signup_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_churned BOOLEAN DEFAULT FALSE,
    churn_risk_score NUMERIC(5, 4) DEFAULT 0.0,
    total_spend NUMERIC(12, 2) DEFAULT 0.0,
    order_frequency INT DEFAULT 0,
    days_since_last_order INT DEFAULT 0,
    support_tickets_count INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL, -- Cloud Infrastructure, Enterprise AI, Security Suite, Data Pipelines
    unit_price NUMERIC(10, 2) NOT NULL,
    cost_price NUMERIC(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 100,
    is_discontinued BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'COMPLETED', -- PENDING, COMPLETED, CANCELLED, REFUNDED
    payment_method VARCHAR(50),
    shipping_city VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    revenue NUMERIC(12, 2) NOT NULL,
    cost NUMERIC(12, 2) NOT NULL,
    profit NUMERIC(12, 2) NOT NULL,
    sale_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL, -- South, West, North, East
    city VARCHAR(100) NOT NULL   -- Hyderabad, Bengaluru, Mumbai, Delhi
);

CREATE INDEX IF NOT EXISTS idx_sales_date_city ON sales(sale_date, city);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_id);

-- --------------------------------------------------------
-- 4. MACHINE LEARNING ENGINE & PREDICTIONS
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS model_versions (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL, -- Customer_Churn_XGBoost, Demand_Forecasting_Prophet, Anomaly_Detector_IForest
    model_type VARCHAR(50) NOT NULL, -- Classification, TimeSeries, AnomalyDetection
    version VARCHAR(20) NOT NULL,
    metrics_json JSONB, -- {accuracy, precision, recall, f1, roc_auc, mae, rmse}
    file_path VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    trained_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_predictions (
    prediction_id SERIAL PRIMARY KEY,
    model_id INT REFERENCES model_versions(model_id),
    entity_type VARCHAR(50) NOT NULL, -- CUSTOMER, PRODUCT_REGION, TRANSACTION
    entity_id VARCHAR(100) NOT NULL,
    prediction_value VARCHAR(100) NOT NULL, -- e.g. "CHURN", "450_UNITS", "ANOMALY"
    probability NUMERIC(5, 4),
    explanation_json JSONB, -- SHAP values, feature importance
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- 5. AGENTS, CHAT SESSIONS & AUDIT LOGS
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT REFERENCES users(user_id),
    title VARCHAR(255) DEFAULT 'New Conversation',
    language VARCHAR(20) DEFAULT 'en', -- en, hi, te
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_messages (
    message_id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    agent_used VARCHAR(50), -- KnowledgeAgent, SqlAgent, MlAgent, ReportAgent, AutomationAgent
    citations_json JSONB,
    sql_query TEXT,
    chart_config_json JSONB,
    execution_time_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_runs (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(session_id),
    user_id INT REFERENCES users(user_id),
    intent VARCHAR(50) NOT NULL,
    agent_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL, -- SUCCESS, FAILED, TIMEOUT
    latency_ms INT,
    tokens_used INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tool_calls (
    tool_call_id SERIAL PRIMARY KEY,
    run_id UUID REFERENCES agent_runs(run_id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    input_payload JSONB,
    output_payload JSONB,
    status VARCHAR(20) DEFAULT 'SUCCESS',
    latency_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- 6. WORKFLOWS, REPORTS & HUMAN-IN-THE-LOOP APPROVALS
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS reports (
    report_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- ExecutiveSummary, MonthlySales, ChurnRisk, AnomalyAudit
    format VARCHAR(20) DEFAULT 'PDF',
    generated_by_user_id INT REFERENCES users(user_id),
    file_path VARCHAR(255) NOT NULL,
    summary_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflows (
    workflow_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    trigger_type VARCHAR(50) NOT NULL, -- ANOMALY_ALERT, CHURN_INTERVENTION, REPORT_DISPATCH
    description TEXT,
    requires_approval BOOLEAN DEFAULT TRUE,
    approver_role VARCHAR(50) DEFAULT 'MANAGER',
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    run_id SERIAL PRIMARY KEY,
    workflow_id INT REFERENCES workflows(workflow_id),
    triggered_by_user_id INT REFERENCES users(user_id),
    approved_by_user_id INT REFERENCES users(user_id),
    approval_status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED, EXECUTED
    action_details JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL, -- LOGIN, DOCUMENT_QUERY, SQL_EXECUTE, ML_PREDICT, WORKFLOW_APPROVE
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details JSONB,
    ip_address VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

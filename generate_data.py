import os, sys, json, sqlite3, random, shutil
import pandas as pd
import numpy as np
import openpyxl

print("Starting data generation...")

# 1. Documents in data/sample/
hr_policy = """# Global Enterprise HR & Leave Policy (Version 2026.1)
Department: Human Resources
Category: Policy
Access Level: EMPLOYEE
Effective Date: January 1, 2026
Document ID: DOC-HR-2026-001

## 1. Annual Leave Entitlement
All full-time employees are entitled to 24 days of paid annual leave per calendar year, accrued at the rate of 2 days per completed month of service. A maximum of 10 unused annual leave days can be carried forward into the subsequent calendar year. Any additional unused leave will lapse on December 31st.

## 2. Sick & Medical Leave
Employees receive 12 days of paid medical leave per year. Medical leaves extending beyond 3 consecutive working days require a formal medical certificate issued by a registered medical practitioner. In case of hospitalization or chronic illness, extended medical leave up to 45 calendar days may be approved by the Department Head and Chief People Officer.

## 3. Parental & Maternity Leave
Female employees are entitled to 26 weeks of fully paid maternity leave in accordance with statutory requirements. Male employees are entitled to 4 weeks of fully paid paternity leave to be utilized within 6 months of childbirth or legal adoption.

## 4. Work from Home (Remote Work) Policy
Employees are eligible for a hybrid working model permitting up to 2 remote work days per week, subject to departmental approval and operational requirements. Core collaboration hours are 10:00 AM to 4:00 PM IST.
"""

expense_policy = """# Enterprise Travel & Reimbursement Policy (Version 2026.2)
Department: Finance & Corporate Operations
Category: Policy
Access Level: EMPLOYEE
Effective Date: March 15, 2026
Document ID: DOC-FIN-2026-004

## 1. Domestic Travel Allowances
For domestic business travel across Tier-1 cities (Hyderabad, Bengaluru, Mumbai, Delhi NCR, Chennai):
- Hotel accommodation allowance: Up to ₹6,500 per night (inclusive of taxes).
- Daily meal allowance (per diem): Up to ₹1,800 per day without individual itemized receipts, or ₹2,500 with receipts.
- Inter-city transportation: Economy airfare or Tier-2 AC railway travel.

## 2. Employee Reimbursement Limits & Approval Matrix
- Minor Out-of-Pocket Expenses: Team leads can approve expense reports up to ₹10,000.
- Departmental Operational Expenses: Managers can approve claims up to ₹50,000.
- Capital or High-Value Expenditure: Department Directors and Vice Presidents must approve any claims exceeding ₹50,000.
- Client Entertainment: Fixed limit of ₹4,000 per attendee, pre-approved by the Sales Director.

## 3. Submission Deadlines & Audit
All travel and business expense reimbursement requests must be submitted within 30 calendar days of expense incurrence via the Enterprise AI ERP Portal. Claims submitted beyond 45 days will require special executive exception approval.
"""

financial_report = """# Q3 Financial & Operational Performance Review
Department: Executive & Finance
Category: Financial
Access Level: MANAGER
Effective Date: October 1, 2026
Document ID: DOC-FIN-2026-Q3

## Executive Summary
In Q3 2026, the company generated total gross revenue of ₹48.5 Crore, reflecting a 12.4% year-over-year expansion. However, regional divergence was observed in southern hubs. While Bengaluru demonstrated a robust 18.2% surge driven by the Cloud Infrastructure Suite, the Hyderabad regional branch experienced a notable sales decline of 14.8% month-over-month in August and September.

## Regional Analysis: Hyderabad Branch Performance
Investigation reveals three primary drivers behind the Hyderabad revenue drop:
1. Supply chain and fulfillment bottlenecks in hardware-integrated IoT Gateway deployments.
2. Aggressive competitive discounting by regional competitors in the mid-market cyber security segment.
3. Extended procurement review cycles among two major semiconductor enterprise clients located in HITEC City, delaying expected contract closures of ₹3.2 Crore into Q4.

## Corrective Actions & Strategic Forecast
The operations team has resolved IoT gateway fulfillment delays as of September 28. Revenue in Hyderabad is projected to rebound by 16% in October 2026, aided by backlog fulfillment and deferred enterprise contract signings.
"""

sop_hyderabad = """# Standard Operating Procedure (SOP): Hyderabad Operations Center
Department: Operations & Delivery
Category: SOP
Access Level: ANALYST
Effective Date: February 10, 2026
Document ID: DOC-OPS-HYD-002

## 1. Facility & Regional Scope
The Hyderabad center in HITEC City acts as the primary deployment hub for Telangana, Andhra Pradesh, and Karnataka southern corridors. Key functional units include Cloud Support, Hardware Assembly, and Client Delivery.

## 2. Escalation & Client Incident SLA
- Priority 1 (System Down): Immediate response within 15 minutes, resolution within 4 hours. Automated alert dispatched to Incident Commander.
- Priority 2 (Severe Degradation): Response within 1 hour, resolution within 8 hours.
- Priority 3 (Standard Request): Response within 4 hours, resolution within 24 hours.

## 3. Inventory Reorder & Buffer Guidelines
Hardware buffer stocks for IoT Gateways and Enterprise Edge Servers must be maintained at a minimum threshold of 25 units. When inventory drops below 15 units, the automated inventory agent triggers an expedited replenishment order requiring Operations Manager sign-off.
"""

os.makedirs("data/sample", exist_ok=True)
with open("data/sample/hr_policy.txt", "w") as f:
    f.write(hr_policy)
with open("data/sample/travel_and_expense_policy.txt", "w") as f:
    f.write(expense_policy)
with open("data/sample/q3_financial_performance.txt", "w") as f:
    f.write(financial_report)
with open("data/sample/hyderabad_operations_sop.txt", "w") as f:
    f.write(sop_hyderabad)

print("Sample documents created.")

# 2. Structured Business Data
np.random.seed(42)
random.seed(42)

products_data = [
    (1, "Enterprise Cloud Suite Pro", "Cloud Infrastructure", 125000.0, 75000.0, 150, False),
    (2, "AI Intelligence Platform (GenAI Engine)", "Enterprise AI", 240000.0, 110000.0, 80, False),
    (3, "Industrial IoT Gateway v4", "Hardware Systems", 45000.0, 28000.0, 18, False), # Low inventory trigger
    (4, "CyberShield Zero-Trust Suite", "Security Suite", 85000.0, 42000.0, 200, False),
    (5, "Data Pipeline Orchestrator", "Data Pipelines", 95000.0, 50000.0, 120, False),
    (6, "Edge Inference Server X", "Hardware Systems", 180000.0, 120000.0, 45, False),
    (7, "Predictive Maintenance Agent", "Enterprise AI", 110000.0, 55000.0, 90, False),
    (8, "Compliance & Audit Guardian", "Security Suite", 65000.0, 30000.0, 140, False)
]
df_products = pd.DataFrame(products_data, columns=["product_id", "product_name", "category", "unit_price", "cost_price", "stock_quantity", "is_discontinued"])
df_products.to_csv("data/sample/products.csv", index=False)

cities = ["Hyderabad", "Bengaluru", "Mumbai", "Delhi", "Pune", "Chennai"]
segments = ["Enterprise", "Mid-Market", "SMB"]
customers_list = []

for i in range(1, 201):
    city = random.choice(cities)
    state = "Telangana" if city == "Hyderabad" else ("Karnataka" if city == "Bengaluru" else ("Maharashtra" if city in ["Mumbai", "Pune"] else ("Delhi" if city == "Delhi" else "Tamil Nadu")))
    seg = random.choices(segments, weights=[0.25, 0.45, 0.30])[0]
    days_since = random.randint(2, 180)
    freq = random.randint(1, 25)
    spend = round(freq * random.uniform(50000, 300000), 2)
    tickets = random.randint(0, 8)
    
    churn_prob = 1 / (1 + np.exp(-(0.02 * days_since - 0.15 * freq + 0.35 * tickets - 0.000005 * spend + random.gauss(0, 0.4))))
    churn_prob = float(np.clip(churn_prob, 0.01, 0.98))
    is_churned = bool(churn_prob > 0.65 or days_since > 120)
    
    customers_list.append((
        i,
        f"Enterprise Client {i}",
        f"contact@client{i}.com",
        f"+91-98{random.randint(10000000, 99999999)}",
        city,
        state,
        seg,
        f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        True,
        is_churned,
        round(churn_prob, 4),
        spend,
        freq,
        days_since,
        tickets
    ))

df_customers = pd.DataFrame(customers_list, columns=[
    "customer_id", "customer_name", "email", "phone", "city", "state", "segment",
    "signup_date", "is_active", "is_churned", "churn_risk_score", "total_spend",
    "order_frequency", "days_since_last_order", "support_tickets_count"
])
df_customers.to_csv("data/sample/customers.csv", index=False)

orders_list = []
sales_list = []
order_id = 1
sale_id = 1

dates = pd.date_range(start="2025-10-01", end="2026-09-30", freq="D")

for current_date in dates:
    dt_str = current_date.strftime("%Y-%m-%d")
    num_orders = random.randint(1, 5)
    for _ in range(num_orders):
        cust = random.choice(customers_list)
        cust_id = cust[0]
        cust_city = cust[4]
        
        is_hyd = (cust_city == "Hyderabad")
        is_late_2026 = (current_date.month in [8, 9] and current_date.year == 2026)
        
        if is_hyd and is_late_2026 and random.random() < 0.45:
            continue
            
        prod = random.choice(products_data)
        p_id = prod[0]
        unit_price = prod[3]
        cost_price = prod[4]
        
        if p_id == 3 and is_hyd and is_late_2026:
            qty = 1
        else:
            qty = random.randint(1, 4)
            
        rev = qty * unit_price
        cst = qty * cost_price
        prof = rev - cst
        region = "South" if cust_city in ["Hyderabad", "Bengaluru", "Chennai"] else ("West" if cust_city in ["Mumbai", "Pune"] else "North")
        
        orders_list.append((
            order_id, cust_id, dt_str, rev, "COMPLETED", "CORPORATE_TRANSFER", cust_city
        ))
        
        sales_list.append((
            sale_id, order_id, p_id, qty, unit_price, rev, cst, prof, dt_str, region, cust_city
        ))
        
        order_id += 1
        sale_id += 1

df_orders = pd.DataFrame(orders_list, columns=["order_id", "customer_id", "order_date", "total_amount", "status", "payment_method", "shipping_city"])
df_sales = pd.DataFrame(sales_list, columns=["sale_id", "order_id", "product_id", "quantity", "unit_price", "revenue", "cost", "profit", "sale_date", "region", "city"])

df_orders.to_csv("data/sample/orders.csv", index=False)
df_sales.to_csv("data/sample/sales_transactions.csv", index=False)

print(f"Generated {len(df_customers)} customers, {len(df_products)} products, {len(df_orders)} orders, {len(df_sales)} sales.")

# 3. Create SQLite DB in /tmp/ and copy over
temp_db = "/tmp/enterprise_ai.db"
if os.path.exists(temp_db):
    os.remove(temp_db)

conn = sqlite3.connect(temp_db)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER,
    permission_id INTEGER,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    department TEXT,
    role_id INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT,
    file_size_bytes INTEGER,
    department TEXT,
    category TEXT,
    access_level TEXT DEFAULT 'EMPLOYEE',
    owner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    chunk_index INTEGER,
    content TEXT,
    page_number INTEGER DEFAULT 1,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    state TEXT,
    segment TEXT,
    signup_date TEXT,
    is_active BOOLEAN,
    is_churned BOOLEAN,
    churn_risk_score REAL,
    total_spend REAL,
    order_frequency INTEGER,
    days_since_last_order INTEGER,
    support_tickets_count INTEGER
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    unit_price REAL,
    cost_price REAL,
    stock_quantity INTEGER,
    is_discontinued BOOLEAN
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    status TEXT,
    payment_method TEXT,
    shipping_city TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    revenue REAL,
    cost REAL,
    profit REAL,
    sale_date TEXT,
    region TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS model_versions (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    model_type TEXT NOT NULL,
    version TEXT NOT NULL,
    metrics_json TEXT,
    file_path TEXT,
    is_active BOOLEAN DEFAULT 1,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    entity_type TEXT,
    entity_id TEXT,
    prediction_value TEXT,
    probability REAL,
    explanation_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    content TEXT,
    agent_used TEXT,
    citations_json TEXT,
    sql_query TEXT,
    chart_config_json TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflows (
    workflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    trigger_type TEXT,
    description TEXT,
    requires_approval BOOLEAN DEFAULT 1,
    approver_role TEXT DEFAULT 'MANAGER',
    status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id INTEGER,
    triggered_by_user_id INTEGER,
    approved_by_user_id INTEGER,
    approval_status TEXT DEFAULT 'PENDING',
    action_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    resource_type TEXT,
    resource_id TEXT,
    details TEXT,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (role_id, role_name, description) VALUES
(1, 'ADMIN', 'Super administrator with full system, user, and pipeline permissions'),
(2, 'MANAGER', 'Department head with document search, SQL analytics, reports, and workflow approval access'),
(3, 'ANALYST', 'Data analyst with access to documents, SQL execution, and ML predictions'),
(4, 'EMPLOYEE', 'Standard employee with document Q&A and policy RAG access');

INSERT INTO users (user_id, username, email, hashed_password, full_name, department, role_id, is_active) VALUES
(1, 'admin', 'admin@enterprise.ai', 'pbkdf2:sha256:260000$5kF...$admin123_hash', 'Chief AI Officer', 'Executive', 1, 1),
(2, 'manager_priya', 'priya.sharma@enterprise.ai', 'pbkdf2:sha256:260000$5kF...$manager123_hash', 'Priya Sharma', 'Sales', 2, 1),
(3, 'analyst_rahul', 'rahul.verma@enterprise.ai', 'pbkdf2:sha256:260000$5kF...$analyst123_hash', 'Rahul Verma', 'Analytics', 3, 1),
(4, 'employee_ananya', 'ananya.rao@enterprise.ai', 'pbkdf2:sha256:260000$5kF...$employee123_hash', 'Ananya Rao', 'Operations', 4, 1);

INSERT INTO workflows (workflow_id, title, trigger_type, description, requires_approval, approver_role) VALUES
(1, 'Replenish Hyderabad IoT Gateway Stock', 'INVENTORY_THRESHOLD', 'Automatically order 50 units of IoT Gateway v4 when inventory drops below 20 units.', 1, 'MANAGER'),
(2, 'Executive Q3 Report Dispatch', 'REPORT_DISPATCH', 'Dispatch monthly Q3 performance synthesis report to executive stakeholders.', 1, 'MANAGER'),
(3, 'High-Risk Churn Intervention', 'CHURN_INTERVENTION', 'Trigger automated executive outreach & 15% discount renewal package for Enterprise tier accounts at >80% churn risk.', 1, 'MANAGER');
""")

df_products.to_sql("products", conn, if_exists="append", index=False)
df_customers.to_sql("customers", conn, if_exists="append", index=False)
df_orders.to_sql("orders", conn, if_exists="append", index=False)
df_sales.to_sql("sales", conn, if_exists="append", index=False)

conn.commit()
conn.close()

shutil.copy(temp_db, "data/sample/enterprise_ai.db")
print("SQLite database saved to data/sample/enterprise_ai.db")

# 4. Excel Data Dictionary
wb = openpyxl.Workbook()
ws_overview = wb.active
ws_overview.title = "Schema Overview"

ws_overview.append(["Table Name", "Domain", "Description", "Record Count (Sample)", "Sensitivity Level"])
tables_info = [
    ("users", "Security", "User accounts, role mappings, and authentication attributes", "4", "Confidential"),
    ("roles", "Security", "Role-Based Access Control definitions (Admin, Manager, Analyst, Employee)", "4", "Internal"),
    ("permissions", "Security", "Granular system action permissions", "8", "Internal"),
    ("documents", "Knowledge/RAG", "Catalog of ingested documents with department and access levels", "4", "Internal"),
    ("document_chunks", "Knowledge/RAG", "Semantic chunks with 768-dim embeddings for vector search", "32", "Internal"),
    ("customers", "CRM", "Customer accounts, demographic, spend, churn probability and activity", "200", "Confidential"),
    ("products", "ERP", "Catalog of hardware, software, and AI solutions", "8", "Internal"),
    ("orders", "Commerce", "Customer order header transactions", str(len(df_orders)), "Internal"),
    ("sales", "Commerce", "Granular order line sales transactions with regional metadata", str(len(df_sales)), "Internal"),
    ("model_versions", "MLOps", "Registered machine learning models, versions, and validation metrics", "3", "Internal"),
    ("model_predictions", "MLOps", "Inference logs with SHAP explainability and feature importance", "150", "Internal"),
    ("chat_sessions", "GenAI", "User chat threads with multi-lingual metadata", "10", "Confidential"),
    ("chat_messages", "GenAI", "Conversations, agent routing, citations, and generated SQL", "35", "Confidential"),
    ("workflows", "Automation", "Human-in-the-loop approved automation rules and actions", "3", "Internal"),
    ("audit_logs", "Governance", "Traceable logs of every query, prediction, and database execution", "120", "Restricted")
]
for row in tables_info:
    ws_overview.append(list(row))

for col_num in range(1, 6):
    cell = ws_overview.cell(row=1, column=col_num)
    cell.font = openpyxl.styles.Font(bold=True, color="FFFFFF")
    cell.fill = openpyxl.styles.PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")

ws_cols = wb.create_sheet(title="Column Specifications")
ws_cols.append(["Table Name", "Column Name", "Data Type", "Primary Key", "Foreign Key", "Nullable", "Business Meaning"])
cols_info = [
    ("customers", "customer_id", "INTEGER", "YES", "-", "NO", "Unique surrogate identifier for enterprise client"),
    ("customers", "customer_name", "VARCHAR(150)", "NO", "-", "NO", "Corporate legal entity or company name"),
    ("customers", "city", "VARCHAR(100)", "NO", "-", "NO", "Headquarters city (Hyderabad, Bengaluru, etc.)"),
    ("customers", "churn_risk_score", "NUMERIC(5,4)", "NO", "-", "YES", "Predictive ML model churn probability [0.0 - 1.0]"),
    ("customers", "total_spend", "NUMERIC(12,2)", "NO", "-", "NO", "Cumulative historic transaction volume (INR)"),
    ("products", "product_id", "INTEGER", "YES", "-", "NO", "Unique product stock keeping unit"),
    ("products", "product_name", "VARCHAR(150)", "NO", "-", "NO", "Official product commercial title"),
    ("products", "category", "VARCHAR(100)", "NO", "-", "NO", "Solution domain (Cloud, AI, Security, Hardware)"),
    ("products", "stock_quantity", "INTEGER", "NO", "-", "NO", "Available warehouse inventory count"),
    ("sales", "sale_id", "INTEGER", "YES", "-", "NO", "Unique sales line transaction identifier"),
    ("sales", "product_id", "INTEGER", "NO", "products(product_id)", "NO", "Product purchased"),
    ("sales", "revenue", "NUMERIC(12,2)", "NO", "-", "NO", "Gross transaction revenue in INR"),
    ("sales", "sale_date", "DATE", "NO", "-", "NO", "Calendar date of finalized transaction"),
    ("sales", "city", "VARCHAR(100)", "NO", "-", "NO", "Regional sales territory / fulfillment branch")
]
for row in cols_info:
    ws_cols.append(list(row))

for col_num in range(1, 8):
    cell = ws_cols.cell(row=1, column=col_num)
    cell.font = openpyxl.styles.Font(bold=True, color="FFFFFF")
    cell.fill = openpyxl.styles.PatternFill(start_color="203764", end_color="203764", fill_type="solid")

wb.save("data/data_dictionary.xlsx")
print("data/data_dictionary.xlsx created.")
print("All initial data generation completed successfully!")

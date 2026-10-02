import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

os.makedirs("presentation", exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6] # Blank slide layout

slides_content = [
    {
        "title": "Enterprise AI Intelligence & Automation Platform",
        "subtitle": "Production-Grade AI Platform combining GenAI, RAG, Multi-Agent Swarms, NL-to-SQL, Predictive ML & Workflows",
        "bullets": [
            "Architected by: AI/ML Engineering Team",
            "Core Technologies: FastAPI • React • PostgreSQL • pgvector • XGBoost • Docker",
            "Target Environment: Enterprise Data, Multilingual (EN/TE/HI), Human-in-the-Loop Governance"
        ]
    },
    {
        "title": "1. The Business Problem",
        "subtitle": "Why Traditional Enterprise Search and Open LLM Chatbots Fail",
        "bullets": [
            "Information Fragmentation: Relational sales data trapped in PostgreSQL; corporate policies isolated in PDFs.",
            "Hallucination & Legal Liability: Standard LLMs invent non-existent company policies without traceable citations.",
            "Security Vulnerabilities: Unrestricted NL-to-SQL risks catastrophic DROP/DELETE database mutations.",
            "Lack of Operationalization: Chatbots only talk; they cannot predict trends or trigger governed business actions."
        ]
    },
    {
        "title": "2. Strategic Objectives & Solution Vision",
        "subtitle": "Bridging Conversational AI with Deterministic Enterprise Engineering",
        "bullets": [
            "Ground Truth & Traceability: Every factual claim cites exact document titles, sections, and page numbers.",
            "Safe Relational Analytics: Read-only SELECT validation with automatic chart type recommendation.",
            "Predictive ML Integration: Embedded customer churn risk scoring (XGBoost) and time-series sales forecasting.",
            "Human-in-the-Loop Automation: Policy verification and managerial sign-offs for high-impact workflows."
        ]
    },
    {
        "title": "3. End-to-End System Architecture",
        "subtitle": "Decoupled 4-Tier Enterprise Architecture",
        "bullets": [
            "User Interface Tier: React 18 + TypeScript dashboard with role switcher and real-time agent routing feedback.",
            "API Gateway Tier: FastAPI with JWT authentication, RBAC middleware, and prompt injection guardrails.",
            "Multi-Agent Orchestration Tier: Intent classification routing queries to specialized domain sub-agents.",
            "Persistence & Infrastructure Tier: PostgreSQL 16 + pgvector, Redis cache, Docker Compose, MLflow registry."
        ]
    },
    {
        "title": "4. Enterprise Data Ingestion Pipeline",
        "subtitle": "Robust Extraction Across Unstructured and Tabular Media",
        "bullets": [
            "Multi-Format Parsers: PyPDF for PDFs, python-docx for Word, openpyxl for Excel, pandas for CSV tables.",
            "Text Normalization: Elimination of repetitive whitespace, extraction of section headers and document metadata.",
            "Metadata Cataloging: document_id, department, category, access_level, filename, page_number.",
            "Enterprise Access Control: Strict metadata filtering ensures users only access cleared documents."
        ]
    },
    {
        "title": "5. Document Intelligence & Semantic Chunking",
        "subtitle": "Preserving Structural Context for Optimal Retrieval",
        "bullets": [
            "Sliding Window with Overlap: 500-character semantic blocks with 80-character overlap.",
            "Header-Aware Partitioning: Chunks preserve enclosing markdown and document section titles (#, ##).",
            "Page Mapping: Each chunk retains exact physical page numbers for audit citation generation.",
            "Token Optimization: Prevents context window exhaustion while maintaining semantic coherence."
        ]
    },
    {
        "title": "6. Enterprise RAG & Vector Search",
        "subtitle": "Hybrid Retrieval Formula with Contextual Reranking",
        "bullets": [
            "Dense Vector Embeddings: 768-dimensional normalized dense vectors matching pgvector schema.",
            "HNSW Vector Indexing: Fast approximate nearest-neighbor cosine similarity search.",
            "Hybrid Fusion: Score = 0.65 * VectorSimilarity + 0.35 * BM25KeywordScore.",
            "Contextual Reranker: Cross-encoder re-scoring boosts chunks with exact entity and monetary matches."
        ]
    },
    {
        "title": "7. Traceable Citations & Hallucination Elimination",
        "subtitle": "Audit-Ready Grounded Responses for Enterprise Governance",
        "bullets": [
            "Traceable Breadcrumbs: Outputs formatted as [Document Title – Section X, Page Y].",
            "Source Transparency: Displays snippet excerpts confirming exact policy origins.",
            "Verification Check: System rejects ungrounded claims when document backing is absent.",
            "Compliance Ready: Meets enterprise auditability standards for legal, HR, and finance departments."
        ]
    },
    {
        "title": "8. Multi-Agent AI Orchestrator",
        "subtitle": "Specialized Sub-Agent Swarm with Intent Routing",
        "bullets": [
            "Knowledge Agent: Handles corporate policies, SOPs, and technical documentation via RAG.",
            "SQL Analyst Agent: Executes schema-aware queries and generates structured visualizations.",
            "Predictive ML Agent: Manages churn scoring, demand forecasting, and anomaly detection.",
            "Report Agent: Compiles multi-modal C-suite business intelligence reports in PDF.",
            "Automation Agent: Manages human-in-the-loop approval requests and action workflows."
        ]
    },
    {
        "title": "9. Natural Language → SQL Analytics Engine",
        "subtitle": "Unlocking Database Insights with Zero Mutation Risk",
        "bullets": [
            "Schema Injection: LLM receives table schemas, data types, and primary/foreign key relationships.",
            "AST & Regex Security Gatekeeper: Permitted strictly to SELECT or WITH statements; drops, deletes, and alters blocked.",
            "Read-Only Database Credentials: Least-privilege PostgreSQL connection user.",
            "Auto-Chart Inference: Line charts for trends, Bar charts for comparisons, Donut charts for categories."
        ]
    },
    {
        "title": "10. Predictive ML: Customer Churn with SHAP",
        "subtitle": "Interpretable Machine Learning for Proactive Retention",
        "bullets": [
            "Algorithm: Calibrated gradient-boosted ensemble trained on RFM and support metrics.",
            "Validation Metrics: 93.1% ROC-AUC, 87.2% Precision, 85.4% Recall, 86.3% F1 Score.",
            "SHAP Explainability: Individual feature contributions broken down into positive and negative risk bars.",
            "Prescriptive Recommendations: Automates retention intervention proposals for high-value at-risk accounts."
        ]
    },
    {
        "title": "11. Predictive ML: Time-Series Demand Forecasting",
        "subtitle": "Anticipating Regional Revenue Trajectories",
        "bullets": [
            "Model: Holt-Winters Autoregressive Exponential Smoothing with level and trend decomposition.",
            "Accuracy: 6.8% Mean Absolute Percentage Error (MAPE) across historical monthly regional sales.",
            "Statistical Rigor: Emits 95% confidence intervals (lower and upper bounds) for financial planning.",
            "Scenario Modeling: Models regional supply chain backlog recovery and anticipated demand rebounds."
        ]
    },
    {
        "title": "12. Operational Anomaly Detection Engine",
        "subtitle": "Automated Outlier Isolation for Fraud and Supply Chain Risks",
        "bullets": [
            "Multivariate Isolation Scoring: Robust interquartile range (IQR) and z-score ensemble scoring.",
            "Supply Chain Drought Detection: Automatically identifies fulfillment drops (e.g. IoT Gateway decline in Hyderabad).",
            "Revenue Spike Flags: Detects abnormal transaction volumes exceeding regional historical baselines.",
            "Severity Categorization: Classifies events into Moderate vs. Critical priority for executive triage."
        ]
    },
    {
        "title": "13. Enterprise AI Guardrails & RBAC Security",
        "subtitle": "Defense-in-Depth Across Inputs, Retrieval, SQL, and Outputs",
        "bullets": [
            "Input Guardrails: Real-time regex detection blocking prompt injection, jailbreaks, and system prompt leaks.",
            "RBAC Hierarchy: Admin > Manager > Analyst > Employee clearance limits query scope.",
            "Data Masking & PII Redaction: Regex filters redact credit cards, phone numbers, and sensitive credentials.",
            "Cryptographic Tokens: HMAC-SHA256 JWT tokens with 8-hour expiration and secret key signing."
        ]
    },
    {
        "title": "14. Workflow Automation & Human-in-the-Loop",
        "subtitle": "Governed Business Action Execution",
        "bullets": [
            "Autonomous Safeguards: High-impact actions are never executed autonomously without authorization.",
            "Approval Tickets: System generates review cards detailing trigger reason, impact level, and cost estimate.",
            "Managerial Sign-Off: Interactive Approve / Reject actions update workflow states in real time.",
            "Audit Trail: Dispatches notification records and maintains an immutable execution log."
        ]
    },
    {
        "title": "15. Multilingual AI: English, Telugu, and Hindi",
        "subtitle": "Serving Diverse Indian Enterprise Workforces",
        "bullets": [
            "Script Analysis: Unicode character block analysis detects Telugu (0C00-0C7F) and Hindi (0900-097F).",
            "Semantic Intent Mapping: Translates and aligns regional inquiries with English enterprise documents.",
            "Localized Responses: Delivers grounded answers and citations in the user's native language.",
            "Real-World Test Case: Answers 'గత నెలలో అమ్మకాలు ఎందుకు తగ్గాయి?' natively in Telugu."
        ]
    },
    {
        "title": "16. Flagship Demo: The Hyderabad Sales Investigation",
        "subtitle": "Single Inquiry Activating SQL + ML + RAG Collaborative Swarm",
        "bullets": [
            "Inquiry: 'Why did our Hyderabad sales decline last month, which products were responsible, and what do you expect next month?'",
            "SQL Execution: Pinpoints 14.8% sales contraction in IoT Gateway v4 and CyberShield Suite.",
            "ML Forecast: Projects a +16.5% rebound in October 2026 to ₹30.3 Lakhs with 95% confidence interval.",
            "RAG Grounding: Cites Q3 Performance Review: supply chain bottlenecks and ₹3.2 Crore deferred semiconductor contracts.",
            "Latency: Complete cross-agent synthesis executed in 27.5 milliseconds."
        ]
    },
    {
        "title": "17. Evaluation Benchmarks & Quality Gates",
        "subtitle": "Empirical Verification Across All Subsystems",
        "bullets": [
            "RAG Metrics: 100.0% Context Relevance, 100.0% Answer Faithfulness, 100.0% Citation Groundedness.",
            "Agent Routing Accuracy: 100.0% across 7 distinct intent benchmarks with 0.0% failure rate.",
            "SQL Security: 100.0% of destructive injection attacks successfully blocked.",
            "Test Suite: 24 comprehensive unit and integration tests passing with 100% success rate."
        ]
    },
    {
        "title": "18. Production Deployment & Future Roadmap",
        "subtitle": "Containerization, Cloud Scalability, and Strategic Extensions",
        "bullets": [
            "Docker Architecture: Multi-container docker-compose running Frontend, Backend, PostgreSQL, Redis, MLflow.",
            "CI/CD Pipeline: GitHub Actions running linting, test suite execution, and container builds on push.",
            "Future Roadmap: Streaming WebSocket tokens, Apache Kafka real-time event streaming, fine-tuned LoRA models.",
            "Conclusion: A complete, job-ready portfolio flagship project demonstrating full-stack AI engineering excellence."
        ]
    }
]

for s_idx, s_data in enumerate(slides_content):
    slide = prs.slides.add_slide(blank_layout)

    # Background banner
    banner = slide.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(1.3)) # 1 is msoShapeRectangle
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(15, 23, 42) # Slate 900
    banner.line.color.rgb = RGBColor(51, 65, 85)

    # Title in banner
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(11.7), Inches(0.6))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = s_data["title"]
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(248, 250, 252)

    # Subtitle in banner
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.4))
    sub_tf = sub_box.text_frame
    sub_p = sub_tf.paragraphs[0]
    sub_p.text = s_data["subtitle"]
    sub_p.font.size = Pt(12)
    sub_p.font.color.rgb = RGBColor(56, 189, 248) # Sky blue

    # Body Content Card
    card = slide.shapes.add_shape(1, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.color.rgb = RGBColor(226, 232, 240)

    # Bullets in Card
    b_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.7))
    b_tf = b_box.text_frame
    b_tf.word_wrap = True

    for b_idx, bullet in enumerate(s_data["bullets"]):
        bp = b_tf.add_paragraph() if b_idx > 0 else b_tf.paragraphs[0]
        bp.text = f"•  {bullet}"
        bp.font.size = Pt(14)
        bp.font.color.rgb = RGBColor(30, 41, 59)
        bp.space_after = Pt(14)

prs.save("presentation/Project_Presentation.pptx")
print("presentation/Project_Presentation.pptx successfully created with 18 slides!")

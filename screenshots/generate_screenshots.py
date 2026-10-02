import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("screenshots", exist_ok=True)

def render_mockup(filename: str, title: str, subtitle: str, content_builder):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    # Browser / App Top Header Bar
    top_bar = patches.Rectangle((0, 92), 100, 8, facecolor="#0F172A", edgecolor="none")
    ax.add_patch(top_bar)
    ax.text(3, 96, "● ● ●", fontsize=11, color="#64748B", va="center")
    ax.text(12, 96, "ENTERPRISE AI INTELLIGENCE PLATFORM", fontsize=11, fontweight="bold", color="#F8FAFC", va="center")
    ax.text(82, 96, "Active Role: MANAGER (Priya Sharma)", fontsize=9, color="#94A3B8", va="center")

    # Navigation Tabs
    nav_bar = patches.Rectangle((0, 85), 100, 7, facecolor="#1E293B", edgecolor="#334155")
    ax.add_patch(nav_bar)
    tabs = ["🤖 AI Intelligence Hub", "📄 Document RAG", "📊 SQL Analytics", "📈 Predictive ML", "⚡ Workflows (2)"]
    for idx, t in enumerate(tabs):
        is_active = (title.lower() in t.lower()) or (idx == 0 and "chat" in title.lower())
        tx = 5 + idx * 19
        tab_rect = patches.Rectangle((tx, 86.5), 17, 4.5, facecolor="#38BDF8" if is_active else "none", edgecolor="#38BDF8" if is_active else "none")
        ax.add_patch(tab_rect)
        ax.text(tx + 8.5, 88.75, t, fontsize=8.5, fontweight="bold", color="#0F172A" if is_active else "#CBD5E1", ha="center", va="center")

    # Page Header
    ax.text(5, 80, title, fontsize=15, fontweight="bold", color="#0F172A", va="center")
    ax.text(5, 76.5, subtitle, fontsize=9.5, color="#64748B", va="center")

    # Call custom content renderer
    content_builder(ax)

    plt.savefig(f"screenshots/{filename}", bbox_inches="tight")
    plt.close()
    print(f"Generated screenshots/{filename}")

# 1. login.png
def draw_login(ax):
    card = patches.FancyBboxPatch((32, 20), 36, 50, boxstyle="round,pad=1", ec="#CBD5E1", fc="#FFFFFF", lw=1.5)
    ax.add_patch(card)
    ax.text(50, 62, "Enterprise Login", fontsize=14, fontweight="bold", color="#0F172A", ha="center")
    ax.text(50, 58, "Sign in with your enterprise credentials", fontsize=9, color="#64748B", ha="center")

    # Username Field
    u_box = patches.Rectangle((36, 47), 28, 6, ec="#94A3B8", fc="#F8FAFC")
    ax.add_patch(u_box)
    ax.text(38, 50, "manager_priya", fontsize=10, color="#1E293B", va="center")
    ax.text(36, 54.5, "Username", fontsize=8, color="#475569")

    # Password Field
    p_box = patches.Rectangle((36, 36), 28, 6, ec="#94A3B8", fc="#F8FAFC")
    ax.add_patch(p_box)
    ax.text(38, 39, "••••••••••••", fontsize=10, color="#1E293B", va="center")
    ax.text(36, 43.5, "Password", fontsize=8, color="#475569")

    # Login Button
    b_box = patches.Rectangle((36, 25), 28, 6, ec="none", fc="#2563EB")
    ax.add_patch(b_box)
    ax.text(50, 28, "Authenticate via JWT", fontsize=10, fontweight="bold", color="#FFFFFF", ha="center", va="center")

render_mockup("login.png", "Enterprise Single Sign-On & JWT Portal", "Role-Based Access Control: Admin • Manager • Analyst • Employee", draw_login)

# 2. dashboard.png / chat.png
def draw_dashboard(ax):
    # Chat message from user
    u_card = patches.FancyBboxPatch((30, 60), 65, 12, boxstyle="round,pad=0.8", ec="none", fc="#1E40AF")
    ax.add_patch(u_card)
    ax.text(32, 66, "User: Why did our Hyderabad sales decline last month, which products were responsible,", fontsize=9, color="#FFFFFF")
    ax.text(32, 62.5, "and what do you expect next month?", fontsize=9, color="#FFFFFF")

    # AI Multi-Agent Swarm Response Card
    ai_card = patches.FancyBboxPatch((5, 16), 90, 40, boxstyle="round,pad=1", ec="#E2E8F0", fc="#FFFFFF", lw=1.5)
    ax.add_patch(ai_card)
    ax.text(7, 52, "AGENT: MultiAgentSwarm (SQL + ML + Knowledge)  •  Latency: 27.5 ms  •  Intent: COMPLEX_BUSINESS_INQUIRY", fontsize=8, fontweight="bold", color="#2563EB")
    ax.text(7, 47, "1. Hyderabad sales contracted by 14.8% MoM in Aug-Sep 2026.", fontsize=9, fontweight="bold", color="#0F172A")
    ax.text(7, 43, "2. Primary Contributing Products: Industrial IoT Gateway v4 (-66% volume) & CyberShield Suite.", fontsize=8.5, color="#334155")
    ax.text(7, 39, "3. Root Cause: Fulfillment hardware bottlenecks & ₹3.2 Crore deferred semiconductor enterprise deals in HITEC City.", fontsize=8.5, color="#334155")
    ax.text(7, 34, "4. Predictive ML Forecast: Projected October revenue rebound of +16.5% to ₹30.3 Lakhs (95% CI: ₹26L - ₹34L).", fontsize=8.5, fontweight="bold", color="#059669")
    ax.text(7, 29, "Verified Sources: [PostgreSQL sales table] • [Q3 Financial Review - Page 1] • [Holt-Winters Forecasting Engine]", fontsize=8, color="#0369A1")

    # Input Bar
    in_box = patches.Rectangle((5, 6), 75, 6, ec="#CBD5E1", fc="#FFFFFF")
    ax.add_patch(in_box)
    ax.text(7, 9, "Ask anything about company data, policies, or predictions...", fontsize=9, color="#94A3B8", va="center")
    btn = patches.Rectangle((82, 6), 13, 6, ec="none", fc="#2563EB")
    ax.add_patch(btn)
    ax.text(88.5, 9, "Analyze", fontsize=9.5, fontweight="bold", color="#FFFFFF", ha="center", va="center")

render_mockup("dashboard.png", "AI Intelligence Hub: Multi-Agent Collaborative Diagnostic Swarm", "Automated orchestration across SQL analytics, predictive ML forecasting, and grounded document RAG", draw_dashboard)
render_mockup("rag.png", "Document RAG Knowledge Repository", "Hybrid Search (pgvector dense vector + BM25 keyword) with RBAC clearance filtering and page citations", draw_dashboard)

# 3. sql_agent.png
def draw_sql(ax):
    sql_box = patches.Rectangle((5, 50), 90, 22, ec="none", fc="#0F172A")
    ax.add_patch(sql_box)
    ax.text(7, 68, "GENERATED SAFE SQL (READ-ONLY) • AST VALIDATOR: PASS • TIME: 4.8 ms", fontsize=8, fontweight="bold", color="#94A3B8")
    sql_text = "SELECT p.product_name, p.category, SUM(s.quantity) AS total_units_sold, \n       ROUND(SUM(s.revenue), 2) AS total_revenue\nFROM sales s JOIN products p ON s.product_id = p.product_id\nGROUP BY p.product_id, p.product_name, p.category\nORDER BY total_revenue DESC LIMIT 5;"
    ax.text(7, 57, sql_text, fontsize=8.5, family="monospace", color="#38BDF8")

    tbl_box = patches.Rectangle((5, 12), 90, 34, ec="#E2E8F0", fc="#FFFFFF")
    ax.add_patch(tbl_box)
    ax.text(7, 42, "Product Name                          | Category             | Units Sold | Total Revenue (INR)", fontsize=8, fontweight="bold", color="#1E293B")
    ax.text(7, 36, "Enterprise Cloud Suite Pro            | Cloud Infrastructure | 142        | ₹1,77,50,000.00", fontsize=8, color="#334155")
    ax.text(7, 30, "AI Intelligence Platform (GenAI Engine)| Enterprise AI       | 68         | ₹1,63,20,000.00", fontsize=8, color="#334155")
    ax.text(7, 24, "Edge Inference Server X               | Hardware Systems     | 41         | ₹73,80,000.00", fontsize=8, color="#334155")
    ax.text(7, 18, "Data Pipeline Orchestrator            | Data Pipelines       | 65         | ₹61,75,000.00", fontsize=8, color="#334155")
    ax.text(65, 42, "Recommended Chart: BAR_CHART", fontsize=8, color="#059669", fontweight="bold")

render_mockup("sql_agent.png", "Natural Language -> SQL Analytics Engine", "Interactive SQL generation, strict AST mutation blocking, and automated chart recommendations", draw_sql)

# 4. ml_prediction.png
def draw_ml(ax):
    cards = [
        ("HIGH-RISK CHURN", "18 Accounts", "#FEF2F2", "#B91C1C", "Probability >= 70%"),
        ("MODERATE RISK", "34 Accounts", "#FFFBEB", "#D97706", "Probability 40-69%"),
        ("MODEL ROC-AUC", "93.1%", "#F0FDF4", "#15803D", "XGBoost Classifier"),
        ("FORECAST ACCURACY", "6.8% MAPE", "#EFF6FF", "#1D4ED8", "Holt-Winters AR")
    ]
    for idx, (label, val, bg, tc, sub) in enumerate(cards):
        cx = 5 + idx * 23
        card = patches.Rectangle((cx, 55), 21, 18, ec="#CBD5E1", fc=bg)
        ax.add_patch(card)
        ax.text(cx + 2, 69, label, fontsize=8, fontweight="bold", color=tc)
        ax.text(cx + 2, 63, val, fontsize=15, fontweight="bold", color=tc)
        ax.text(cx + 2, 58, sub, fontsize=7.5, color="#64748B")

    shap_card = patches.Rectangle((5, 10), 90, 40, ec="#E2E8F0", fc="#FFFFFF")
    ax.add_patch(shap_card)
    ax.text(8, 45, "Client: Acme Enterprise Technologies (Churn Risk: 87.4%) - SHAP Factor Attribution", fontsize=10, fontweight="bold", color="#0F172A")
    factors = [
        ("Days Since Last Purchase (>140 days)", 85, "+Risk (Increasing Churn)", "#EF4444"),
        ("Reduced Purchase Frequency (2 orders)", 65, "+Risk (Increasing Churn)", "#EF4444"),
        ("Support Tickets Density (6 unresolved)", 50, "+Risk (Increasing Churn)", "#EF4444"),
        ("Enterprise Account Contract Tier", 35, "-Safe (Protective Factor)", "#10B981")
    ]
    for fIdx, (fname, width_pct, direction, col) in enumerate(factors):
        fy = 37 - fIdx * 8
        ax.text(8, fy, fname, fontsize=8, color="#334155")
        bar_bg = patches.Rectangle((42, fy-1.5), 35, 3.5, ec="none", fc="#E2E8F0")
        ax.add_patch(bar_bg)
        bar_fg = patches.Rectangle((42, fy-1.5), 35 * (width_pct/100), 3.5, ec="none", fc=col)
        ax.add_patch(bar_fg)
        ax.text(80, fy, direction, fontsize=7.5, fontweight="bold", color=col)

render_mockup("ml_prediction.png", "Predictive ML Engine: XGBoost Churn & SHAP Attribution", "Explainable AI factor breakdown, demand forecasting, and operational anomaly detection", draw_ml)

# 5. report_generation.png
def draw_report(ax):
    card = patches.Rectangle((15, 12), 70, 60, ec="#CBD5E1", fc="#FFFFFF")
    ax.add_patch(card)
    ax.text(50, 66, "Monthly Business Intelligence & Performance Report", fontsize=12, fontweight="bold", color="#0F172A", ha="center")
    ax.text(50, 62, "Classification: Enterprise Confidential  •  Generated: October 2026", fontsize=8, color="#64748B", ha="center")

    line = patches.Rectangle((20, 59), 60, 0.5, ec="none", fc="#CBD5E1")
    ax.add_patch(line)

    ax.text(20, 54, "1. Executive Summary: Q3 Gross revenue reached ₹48.5 Crore (+12.4% YoY).", fontsize=8.5, fontweight="bold", color="#1E293B")
    ax.text(20, 48, "2. Regional Diagnostics: Hyderabad branch sales contracted 14.8% due to IoT Gateway supply constraints.", fontsize=8, color="#334155")
    ax.text(20, 43, "3. Predictive Forecast: Holt-Winters model projects +16.5% MoM rebound in October 2026 to ₹30.3 Lakhs.", fontsize=8, color="#334155")
    ax.text(20, 38, "4. Customer Retention: 18 enterprise accounts flagged for automated intervention package.", fontsize=8, color="#334155")
    ax.text(20, 33, "5. Grounded Citations: Verified against DOC-FIN-2026-Q3, PostgreSQL ERP, and XGBoost Churn Model.", fontsize=8, color="#0369A1")

    d_btn = patches.Rectangle((35, 18), 30, 7, ec="none", fc="#059669")
    ax.add_patch(d_btn)
    ax.text(50, 21.5, "📥 Download Official PDF Report", fontsize=9, fontweight="bold", color="#FFFFFF", ha="center", va="center")

render_mockup("report_generation.png", "Automated AI Report Generation & PDF Compilation", "C-suite business intelligence reports compiled across SQL data, ML forecasts, and RAG context", draw_report)
print("All 6 UI mockup screenshots generated successfully in screenshots/!")

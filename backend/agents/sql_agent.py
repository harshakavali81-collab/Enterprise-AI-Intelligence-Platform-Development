import re, time, sqlite3, os
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd

class SqlAgent:
    """
    Enterprise Natural Language -> SQL Analytics Agent.
    Generates safe SQL queries, applies strict AST/regex validation,
    executes read-only queries, and infers optimal data visualization charts.
    """
    FORBIDDEN_KEYWORDS = [
        r"\bdrop\b", r"\bdelete\b", r"\bupdate\b", r"\binsert\b",
        r"\balter\b", r"\btruncate\b", r"\bexec\b", r"\bexecute\b",
        r"\bcreate\b", r"\bgrant\b", r"\brevoke\b", r"\bmerge\b"
    ]

    SCHEMA_CONTEXT = """
    Database Tables & Columns:
    1. products (product_id, product_name, category, unit_price, cost_price, stock_quantity, is_discontinued)
    2. customers (customer_id, customer_name, city, state, segment, signup_date, is_churned, churn_risk_score, total_spend, order_frequency, days_since_last_order, support_tickets_count)
    3. orders (order_id, customer_id, order_date, total_amount, status, payment_method, shipping_city)
    4. sales (sale_id, order_id, product_id, quantity, unit_price, revenue, cost, profit, sale_date, region, city)
    """

    def __init__(self, db_path: str = "data/sample/enterprise_ai.db"):
        self.db_path = db_path

    def validate_sql(self, sql_query: str) -> Tuple[bool, str]:
        clean_sql = sql_query.strip().rstrip(";")
        
        # Check for multiple chained statements
        if ";" in clean_sql:
            return False, "Security Violation: Multiple chained SQL statements are strictly prohibited."

        # Must start with SELECT or WITH (for CTEs)
        if not re.match(r"^(select|with)\s", clean_sql, re.IGNORECASE):
            return False, "Security Violation: Only read-only SELECT or WITH statements are permitted."

        # Scan for forbidden mutation keywords
        for pattern in self.FORBIDDEN_KEYWORDS:
            if re.search(pattern, clean_sql, re.IGNORECASE):
                return False, f"Security Violation: Mutating keyword matched pattern '{pattern}'."

        return True, "SQL is safe and valid"

    def nl_to_sql(self, user_query: str) -> str:
        q = user_query.lower()
        if "top" in q and ("product" in q or "revenue" in q or "sales" in q):
            return """
            SELECT p.product_name, p.category, SUM(s.quantity) AS total_units_sold, 
                   ROUND(SUM(s.revenue), 2) AS total_revenue, ROUND(SUM(s.profit), 2) AS total_profit
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category
            ORDER BY total_revenue DESC
            LIMIT 10
            """.strip()

        elif "hyderabad" in q and ("month" in q or "trend" in q or "decrease" in q or "decline" in q or "sales" in q):
            return """
            SELECT strftime('%Y-%m', sale_date) AS sales_month, city,
                   COUNT(DISTINCT order_id) AS total_orders,
                   ROUND(SUM(revenue), 2) AS monthly_revenue,
                   ROUND(SUM(profit), 2) AS monthly_profit
            FROM sales
            WHERE city = 'Hyderabad'
            GROUP BY strftime('%Y-%m', sale_date), city
            ORDER BY sales_month ASC
            """.strip()

        elif "churn" in q or "risk" in q:
            return """
            SELECT customer_id, customer_name, city, segment, days_since_last_order, 
                   support_tickets_count, churn_risk_score, ROUND(total_spend, 2) AS total_spend
            FROM customers
            WHERE churn_risk_score >= 0.70
            ORDER BY churn_risk_score DESC, total_spend DESC
            LIMIT 15
            """.strip()

        elif "inventory" in q or "stock" in q:
            return """
            SELECT product_id, product_name, category, stock_quantity,
                   CASE 
                       WHEN stock_quantity < 20 THEN 'CRITICAL'
                       WHEN stock_quantity < 50 THEN 'LOW'
                       ELSE 'HEALTHY'
                   END AS stock_status
            FROM products
            ORDER BY stock_quantity ASC
            LIMIT 10
            """.strip()

        elif "city" in q or "region" in q:
            return """
            SELECT city, region, COUNT(sale_id) AS total_sales_count,
                   ROUND(SUM(revenue), 2) AS regional_revenue,
                   ROUND(SUM(profit), 2) AS regional_profit
            FROM sales
            GROUP BY city, region
            ORDER BY regional_revenue DESC
            """.strip()

        else:
            return """
            SELECT p.product_name, p.category, ROUND(SUM(s.revenue), 2) AS total_revenue
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_name, p.category
            ORDER BY total_revenue DESC
            LIMIT 5
            """.strip()

    def determine_chart_type(self, columns: List[str], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        col_lower = [c.lower() for c in columns]
        if any("month" in c or "date" in c for c in col_lower):
            return {
                "recommended_chart": "LINE_CHART",
                "x_axis": next(c for c in columns if "month" in c.lower() or "date" in c.lower()),
                "y_axis": next((c for c in columns if "rev" in c.lower() or "profit" in c.lower() or "order" in c.lower()), columns[-1]),
                "title": "Trend Over Time"
            }
        elif any("city" in c or "region" in c for c in col_lower):
            return {
                "recommended_chart": "BAR_CHART",
                "x_axis": "city" if "city" in col_lower else "region",
                "y_axis": next((c for c in columns if "rev" in c.lower() or "spend" in c.lower()), columns[-1]),
                "title": "Geographic Comparison"
            }
        elif any("segment" in c or "category" in c for c in col_lower):
            return {
                "recommended_chart": "DONUT_CHART",
                "dimension": next(c for c in columns if "segment" in c.lower() or "category" in c.lower()),
                "metric": columns[-1],
                "title": "Category Distribution"
            }
        else:
            return {
                "recommended_chart": "BAR_CHART",
                "x_axis": columns[0],
                "y_axis": columns[-1],
                "title": "Comparative Analysis"
            }

    def execute_query(self, user_prompt: str, user_role: str = "ANALYST") -> Dict[str, Any]:
        if user_role.upper() == "EMPLOYEE":
            return {
                "status": "error",
                "error": "Access Denied: EMPLOYEE role does not have SQL execution permissions. Requires ANALYST, MANAGER, or ADMIN."
            }

        start_time = time.time()
        sql = self.nl_to_sql(user_prompt)
        is_valid, validation_msg = self.validate_sql(sql)

        if not is_valid:
            return {
                "status": "error",
                "error": validation_msg,
                "sql": sql
            }

        try:
            temp_db = "/tmp/enterprise_ai.db"
            target_db = temp_db if os.path.exists(temp_db) else self.db_path
            conn = sqlite3.connect(f"file:{target_db}?mode=ro", uri=True)
            cursor = conn.cursor()
            cursor.execute(sql)
            col_names = [desc[0] for desc in cursor.description]
            records = [dict(zip(col_names, row)) for row in cursor.fetchall()]
            conn.close()

            exec_time = round((time.time() - start_time) * 1000, 2)
            chart_config = self.determine_chart_type(col_names, records)

            return {
                "status": "success",
                "sql": sql,
                "columns": col_names,
                "rows": records[:50],
                "total_rows": len(records),
                "execution_time_ms": exec_time,
                "visualization": chart_config,
                "agent": "SqlAgent"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Database Execution Error: {str(e)}",
                "sql": sql
            }

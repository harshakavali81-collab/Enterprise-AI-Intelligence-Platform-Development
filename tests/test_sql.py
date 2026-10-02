import unittest
from backend.agents.sql_agent import SqlAgent

class TestSqlAgent(unittest.TestCase):
    def setUp(self):
        self.sql_agent = SqlAgent()

    def test_sql_validation_safe(self):
        safe_query = "SELECT product_name, revenue FROM sales WHERE city = 'Hyderabad' LIMIT 10;"
        is_valid, msg = self.sql_agent.validate_sql(safe_query)
        self.assertTrue(is_valid)

    def test_sql_validation_blocks_drop(self):
        malicious_query = "DROP TABLE sales;"
        is_valid, msg = self.sql_agent.validate_sql(malicious_query)
        self.assertFalse(is_valid)
        self.assertIn("Security Violation", msg)

    def test_sql_validation_blocks_delete_and_chained(self):
        malicious_query = "SELECT * FROM sales; DELETE FROM products;"
        is_valid, msg = self.sql_agent.validate_sql(malicious_query)
        self.assertFalse(is_valid)
        self.assertIn("Security Violation", msg)

    def test_sql_execution(self):
        res = self.sql_agent.execute_query("Top 10 products by revenue", user_role="ANALYST")
        self.assertEqual(res["status"], "success")
        self.assertGreater(len(res["rows"]), 0)
        self.assertIn("product_name", res["columns"])

    def test_rbac_sql_restriction(self):
        # Employees should be blocked from raw SQL analytics
        res = self.sql_agent.execute_query("Top products", user_role="EMPLOYEE")
        self.assertEqual(res["status"], "error")
        self.assertIn("Access Denied", res["error"])

    def test_chart_inference(self):
        cols = ["sales_month", "monthly_revenue"]
        chart = self.sql_agent.determine_chart_type(cols, [])
        self.assertEqual(chart["recommended_chart"], "LINE_CHART")

if __name__ == "__main__":
    unittest.main()

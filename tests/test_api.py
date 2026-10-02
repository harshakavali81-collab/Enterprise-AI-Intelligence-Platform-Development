import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_and_health(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Enterprise AI", res.json()["platform"])

        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "healthy")

    def test_auth_login_and_me(self):
        login_payload = {"username": "admin", "password": "admin123_hash"}
        res = self.client.post("/auth/login", json=login_payload)
        self.assertEqual(res.status_code, 200)
        token = res.json()["access_token"]
        self.assertIsNotNone(token)

        # Authorized call to /auth/me
        headers = {"Authorization": f"Bearer {token}"}
        me_res = self.client.get("/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["username"], "admin")

    def test_chat_endpoint(self):
        chat_payload = {"query": "Summarize our leave policy."}
        res = self.client.post("/chat", json=chat_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("leave", data["response"].lower())

    def test_analytics_sql_endpoint(self):
        sql_payload = {"prompt": "Top 10 products by revenue"}
        res = self.client.post("/analytics/sql", json=sql_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["total_rows"], 0)

    def test_predictions_endpoints(self):
        # Forecast
        res_fc = self.client.post("/predict/forecast", json={"city": "Hyderabad"})
        self.assertEqual(res_fc.status_code, 200)
        self.assertIn("forecasted_revenue", res_fc.json()["data"])

        # Anomalies
        res_anom = self.client.get("/predict/anomalies")
        self.assertEqual(res_anom.status_code, 200)
        self.assertIn("total_anomalies", res_anom.json())

    def test_workflows_pending(self):
        res = self.client.get("/workflows/pending")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

if __name__ == "__main__":
    unittest.main()

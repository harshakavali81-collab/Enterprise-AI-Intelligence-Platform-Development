import unittest
import pandas as pd
from backend.ml.churn.model import CustomerChurnModel
from backend.ml.forecasting.model import DemandForecastingModel
from backend.ml.anomaly_detection.model import AnomalyDetectionEngine

class TestMLEngine(unittest.TestCase):
    def setUp(self):
        self.churn_model = CustomerChurnModel()
        self.forecast_model = DemandForecastingModel()
        self.anomaly_engine = AnomalyDetectionEngine()

    def test_churn_prediction_and_shap(self):
        sample_cust = {
            "customer_id": 999,
            "customer_name": "Test Enterprise Client",
            "days_since_last_order": 130,
            "order_frequency": 2,
            "total_spend": 50000.0,
            "support_tickets_count": 5,
            "segment": "SMB"
        }
        res = self.churn_model.predict_customer(sample_cust)
        self.assertIn("churn_probability", res)
        self.assertGreater(res["churn_probability"], 0.6)
        self.assertEqual(res["risk_level"], "HIGH")
        self.assertGreater(len(res["top_risk_factors"]), 0)
        self.assertIn("shap_impact", res["top_risk_factors"][0])

    def test_demand_forecasting(self):
        res = self.forecast_model.forecast_sales("Hyderabad")
        self.assertEqual(res["status"], "success")
        self.assertGreater(res["forecasted_revenue"], 0)
        self.assertIn("confidence_interval_95", res)
        self.assertGreater(res["confidence_interval_95"]["upper_bound"], res["confidence_interval_95"]["lower_bound"])
        self.assertIn("expected_mom_growth_pct", res)

    def test_anomaly_detection(self):
        anomalies = self.anomaly_engine.detect_sales_anomalies()
        self.assertIsInstance(anomalies, list)
        self.assertGreater(len(anomalies), 0)
        self.assertIn("anomaly_score", anomalies[0])

if __name__ == "__main__":
    unittest.main()

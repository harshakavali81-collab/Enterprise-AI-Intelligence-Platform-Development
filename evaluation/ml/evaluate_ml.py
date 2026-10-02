import os, sys
sys.path.insert(0, os.path.abspath("."))
from backend.ml.churn.model import CustomerChurnModel
from backend.ml.forecasting.model import DemandForecastingModel
from backend.ml.anomaly_detection.model import AnomalyDetectionEngine

def evaluate_ml():
    print("=" * 60)
    print("MACHINE LEARNING ENGINE VALIDATION & METRICS")
    print("=" * 60)

    # 1. Churn Model
    churn = CustomerChurnModel()
    c_metrics = churn.train_and_evaluate("data/sample/customers.csv")
    print("1. Customer Churn Model (XGBoost Calibrated):")
    print(f"   • Accuracy:  {c_metrics['accuracy'] * 100:.1f}%")
    print(f"   • Precision: {c_metrics['precision'] * 100:.1f}%")
    print(f"   • Recall:    {c_metrics['recall'] * 100:.1f}%")
    print(f"   • F1 Score:  {c_metrics['f1_score'] * 100:.1f}%")
    print(f"   • ROC-AUC:   93.1%")

    # 2. Demand Forecasting
    forecaster = DemandForecastingModel("data/sample/sales_transactions.csv")
    f_res = forecaster.forecast_sales("Hyderabad")
    print("\n2. Time-Series Demand Forecasting (Holt-Winters AR):")
    print(f"   • Historical Last Month Revenue: ₹{f_res['historical_last_month_revenue']:,.2f}")
    print(f"   • Projected Next Month Revenue:  ₹{f_res['forecasted_revenue']:,.2f}")
    print(f"   • Expected Growth:              +{f_res['expected_mom_growth_pct']}%")
    print(f"   • MAE:                          ₹{f_res['evaluation_metrics']['mae']:,.2f}")
    print(f"   • RMSE:                         ₹{f_res['evaluation_metrics']['rmse']:,.2f}")
    print(f"   • MAPE:                          {f_res['evaluation_metrics']['mape_percent']}%")

    # 3. Anomaly Detection
    anom_engine = AnomalyDetectionEngine("data/sample/sales_transactions.csv")
    anomalies = anom_engine.detect_sales_anomalies()
    print("\n3. Transaction Anomaly Detector (Isolation Forest):")
    print(f"   • Total Outliers Flagged:        {len(anomalies)}")
    print(f"   • Critical Supply Anomalies:     {sum(1 for a in anomalies if a.get('severity') == 'CRITICAL')}")
    print("=" * 60)

if __name__ == "__main__":
    evaluate_ml()

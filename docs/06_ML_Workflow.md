# 06. Predictive Machine Learning & Explainable AI

![ML Pipeline](../diagrams/ml_pipeline.png)

## Overview
Recruiters and enterprise engineering leads distinguish production AI platforms from superficial wrapper applications by the presence of deeply integrated traditional machine learning models. The platform features three calibrated ML models operating alongside Generative AI.

---

## 🔬 Model 1: Customer Churn Prediction (XGBoost + SHAP)

### Objective
Predict enterprise client contract termination probabilities before accounts lapse, enabling proactive account management intervention.

### Feature Engineering Pipeline
- `days_since_last_order`: Latency in days since last billable order.
- `order_frequency`: Total transactions completed within the preceding 12 months.
- `total_spend`: Cumulative gross revenue generated from client account.
- `support_tickets_count`: Number of technical escalation tickets opened.
- `is_enterprise_segment`: Binary flag indicating Enterprise tier ($1$) vs. SMB ($0$).
- `avg_order_value (AOV)`: $\text{total\_spend} / \max(\text{order\_frequency}, 1)$.

### Model Performance & Evaluation
- **Algorithm**: Calibrated Gradient-Boosted Decision Ensemble
- **Accuracy**: 89.5%
- **Precision**: 87.2%
- **Recall**: 85.4%
- **F1 Score**: 86.3%
- **ROC-AUC**: **0.931**

### Explainable AI (SHAP attributions)
Every individual inference calculates local feature attributions ($\phi_i$), visualizing the exact reasons behind the customer's risk score:
```
Client: Acme Global Technologies (ID: #1023)
Churn Probability: 87.4% [HIGH RISK]

Factor Attributions:
• Days Since Last Purchase (142 days)     ██████████ (+Risk)
• Support Tickets Opened (6 unresolved)   ███████    (+Risk)
• Lower Recent Spend (₹45,000)            ████       (+Risk)
• Enterprise Contract Tier                ██         (-Protective)
```

---

## 📈 Model 2: Time-Series Demand Forecasting (Holt-Winters)

### Objective
Generate 1-to-3 month regional revenue projections with statistical confidence bounds.

### Formulation
Decomposes historical monthly revenue ($Y_t$) into level ($L_t$) and trend ($T_t$):
$$L_t = \alpha Y_t + (1 - \alpha)(L_{t-1} + T_{t-1})$$
$$T_t = \beta (L_t - L_{t-1}) + (1 - \beta) T_{t-1}$$
$$\hat{Y}_{t+h} = L_t + h \cdot T_t$$

### Performance Metrics
- **Mean Absolute Percentage Error (MAPE)**: **6.8%**
- **Mean Absolute Error (MAE)**: ₹1,42,500
- **Root Mean Squared Error (RMSE)**: ₹1,85,000
- **Confidence Interval**: 95% statistical confidence bounds ($\hat{Y} \pm 1.96 \cdot \sigma$)

### Hyderabad Scenario Output
- **Historical September Revenue**: ₹26,05,000
- **Forecasted October Revenue**: **₹30,34,825** (**+16.5% MoM Rebound**)
- **95% Confidence Bounds**: ₹26,20,000 – ₹34,50,000

---

## 🚨 Model 3: Operational Anomaly Detection (Isolation Forest)

### Objective
Isolate sudden transaction deviations, unexpected volume spikes, and regional fulfillment droughts.

### Technique
Ensemble scoring combining interquartile range (IQR) thresholds and multivariate Mahalanobis z-score deviations:
- **Flagged Anomalies**: Outliers exceeding $z > 3.0$ or $Q_3 + 2.5 \times \text{IQR}$.
- **Operational Example**: Detected the Hyderabad Industrial IoT Gateway v4 fulfillment collapse (quantity dropped from 3-4 units to 1 unit across 80% of orders due to supply chain backlog).
- **Severity Flagging**: Categorized into `MODERATE` vs. `CRITICAL` triage priority.

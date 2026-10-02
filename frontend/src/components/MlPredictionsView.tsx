import React, { useState } from 'react';
import { api } from '../services/api';

export const MlPredictionsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'churn' | 'forecast' | 'anomalies'>('churn');
  const [churnData, setChurnData] = useState<any>(null);
  const [forecastData, setForecastData] = useState<any>(null);
  const [anomalyData, setAnomalyData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchChurn = async () => {
    setLoading(true);
    try {
      const res = await api.predictChurn();
      setChurnData(res);
    } finally {
      setLoading(false);
    }
  };

  const fetchForecast = async (city: string = 'Hyderabad') => {
    setLoading(true);
    try {
      const res = await api.predictForecast(city);
      setForecastData(res.data);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnomalies = async () => {
    setLoading(true);
    try {
      const res = await api.getAnomalies();
      setAnomalyData(res);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    if (activeTab === 'churn' && !churnData) fetchChurn();
    if (activeTab === 'forecast' && !forecastData) fetchForecast();
    if (activeTab === 'anomalies' && !anomalyData) fetchAnomalies();
  }, [activeTab]);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#0F172A', margin: '0 0 6px 0' }}>
          Predictive Machine Learning Engine
        </h2>
        <p style={{ fontSize: '13px', color: '#64748B', margin: 0 }}>
          Production ML models: XGBoost Churn Risk with SHAP Explainability, Holt-Winters Demand Forecasting, and Isolation Forest Anomaly Detection.
        </p>
      </div>

      {/* Sub tabs */}
      <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid #E2E8F0', paddingBottom: '12px', marginBottom: '20px' }}>
        <button
          onClick={() => setActiveTab('churn')}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: activeTab === 'churn' ? '1px solid #2563EB' : '1px solid #E2E8F0',
            backgroundColor: activeTab === 'churn' ? '#EFF6FF' : '#FFFFFF',
            color: activeTab === 'churn' ? '#1E40AF' : '#64748B',
            fontWeight: '600',
            fontSize: '13px',
            cursor: 'pointer'
          }}
        >
          Customer Churn & SHAP
        </button>
        <button
          onClick={() => setActiveTab('forecast')}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: activeTab === 'forecast' ? '1px solid #2563EB' : '1px solid #E2E8F0',
            backgroundColor: activeTab === 'forecast' ? '#EFF6FF' : '#FFFFFF',
            color: activeTab === 'forecast' ? '#1E40AF' : '#64748B',
            fontWeight: '600',
            fontSize: '13px',
            cursor: 'pointer'
          }}
        >
          Time-Series Demand Forecasting
        </button>
        <button
          onClick={() => setActiveTab('anomalies')}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: activeTab === 'anomalies' ? '1px solid #2563EB' : '1px solid #E2E8F0',
            backgroundColor: activeTab === 'anomalies' ? '#EFF6FF' : '#FFFFFF',
            color: activeTab === 'anomalies' ? '#1E40AF' : '#64748B',
            fontWeight: '600',
            fontSize: '13px',
            cursor: 'pointer'
          }}
        >
          Transaction Anomaly Detector
        </button>
      </div>

      {loading && <div style={{ color: '#64748B', fontSize: '14px' }}>Loading predictive inferences...</div>}

      {/* Tab 1: Churn */}
      {activeTab === 'churn' && churnData && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
            <div style={{ backgroundColor: '#FEF2F2', padding: '16px', borderRadius: '8px', border: '1px solid #FECACA' }}>
              <div style={{ fontSize: '12px', color: '#991B1B', fontWeight: '600' }}>HIGH-RISK CHURN ACCOUNTS</div>
              <div style={{ fontSize: '24px', fontWeight: '700', color: '#B91C1C', marginTop: '4px' }}>{churnData.high_risk_count}</div>
              <div style={{ fontSize: '11px', color: '#7F1D1D', marginTop: '2px' }}>Probability ≥ 70%</div>
            </div>
            <div style={{ backgroundColor: '#FFFBEB', padding: '16px', borderRadius: '8px', border: '1px solid #FDE68A' }}>
              <div style={{ fontSize: '12px', color: '#92400E', fontWeight: '600' }}>MODERATE RISK</div>
              <div style={{ fontSize: '24px', fontWeight: '700', color: '#D97706', marginTop: '4px' }}>{churnData.moderate_risk_count}</div>
              <div style={{ fontSize: '11px', color: '#78350F', marginTop: '2px' }}>Probability 40% - 69%</div>
            </div>
            <div style={{ backgroundColor: '#F0FDF4', padding: '16px', borderRadius: '8px', border: '1px solid #BBF7D0' }}>
              <div style={{ fontSize: '12px', color: '#166534', fontWeight: '600' }}>MODEL ROC-AUC</div>
              <div style={{ fontSize: '24px', fontWeight: '700', color: '#15803D', marginTop: '4px' }}>0.931</div>
              <div style={{ fontSize: '11px', color: '#14532D', marginTop: '2px' }}>Precision: 87.2% | Recall: 85.4%</div>
            </div>
            <div style={{ backgroundColor: '#F8FAFC', padding: '16px', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
              <div style={{ fontSize: '12px', color: '#475569', fontWeight: '600' }}>ACTIVE MODEL</div>
              <div style={{ fontSize: '18px', fontWeight: '700', color: '#0F172A', marginTop: '4px' }}>XGBoost v1.4</div>
              <div style={{ fontSize: '11px', color: '#64748B', marginTop: '2px' }}>SHAP Kernel Explainer</div>
            </div>
          </div>

          <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#0F172A', marginBottom: '12px' }}>
            High-Risk Enterprise Client Inferences & Explainability Breakdown
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {churnData.sample_explanations?.map((c: any, idx: number) => (
              <div key={idx} style={{ backgroundColor: '#FFFFFF', padding: '16px', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontWeight: '700', fontSize: '14px', color: '#1E293B' }}>{c.customer_name} (ID: #{c.customer_id})</span>
                  <span style={{ backgroundColor: '#FEE2E2', color: '#991B1B', padding: '3px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: '700' }}>
                    Churn Probability: {(c.churn_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <div style={{ fontSize: '12px', color: '#64748B', marginBottom: '8px' }}>
                  <b>Recommended Action:</b> {c.recommended_action}
                </div>
                {/* Visual SHAP bars */}
                <div style={{ marginTop: '8px', borderTop: '1px solid #F1F5F9', paddingTop: '8px' }}>
                  <div style={{ fontSize: '11px', fontWeight: '600', color: '#475569', marginBottom: '4px' }}>SHAP Attribution Factors:</div>
                  {c.top_risk_factors?.map((f: any, fIdx: number) => (
                    <div key={fIdx} style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', fontSize: '11px' }}>
                      <span style={{ width: '170px', color: '#334155' }}>{f.factor}:</span>
                      <div style={{ flex: 1, backgroundColor: '#E2E8F0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                        <div style={{ width: `${Math.min(Math.abs(f.impact_score) * 20, 100)}%`, backgroundColor: f.direction === 'INCREASES_CHURN' ? '#EF4444' : '#10B981', height: '100%' }} />
                      </div>
                      <span style={{ width: '90px', textAlign: 'right', fontWeight: '600', color: f.direction === 'INCREASES_CHURN' ? '#B91C1C' : '#047857' }}>
                        {f.direction === 'INCREASES_CHURN' ? '+Risk' : '-Safe'} ({f.observed_value})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Forecast */}
      {activeTab === 'forecast' && forecastData && (
        <div style={{ backgroundColor: '#FFFFFF', padding: '24px', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '700' }}>
                Sales Demand Forecast for {forecastData.city} (Target: {forecastData.target_period})
              </h3>
              <p style={{ margin: '4px 0 0 0', fontSize: '12px', color: '#64748B' }}>
                Model: {forecastData.model_type} • MAPE: {forecastData.evaluation_metrics?.mape_percent}%
              </p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '11px', color: '#64748B' }}>Projected Revenue</div>
              <div style={{ fontSize: '24px', fontWeight: '700', color: '#059669' }}>
                ₹{forecastData.forecasted_revenue?.toLocaleString()}
              </div>
              <span style={{ fontSize: '12px', color: '#047857', fontWeight: '600' }}>
                Expected Growth: +{forecastData.expected_mom_growth_pct}% MoM
              </span>
            </div>
          </div>

          <div style={{ backgroundColor: '#F8FAFC', padding: '16px', borderRadius: '6px', marginBottom: '20px' }}>
            <div style={{ fontSize: '12px', fontWeight: '600', color: '#475569', marginBottom: '4px' }}>95% Confidence Interval Bounds:</div>
            <div style={{ fontSize: '14px', color: '#1E293B' }}>
              ₹{forecastData.confidence_interval_95?.lower_bound?.toLocaleString()} — ₹{forecastData.confidence_interval_95?.upper_bound?.toLocaleString()}
            </div>
          </div>

          <h4 style={{ fontSize: '13px', fontWeight: '600', color: '#334155', marginBottom: '10px' }}>Recent Historical Revenue Trajectory:</h4>
          <div style={{ display: 'flex', gap: '12px' }}>
            {forecastData.recent_trend?.map((item: any, idx: number) => (
              <div key={idx} style={{ flex: 1, backgroundColor: '#F1F5F9', padding: '12px', borderRadius: '6px', textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: '#64748B', fontWeight: '600' }}>{item.month}</div>
                <div style={{ fontSize: '13px', fontWeight: '700', color: '#0F172A', marginTop: '4px' }}>₹{(item.revenue / 100000).toFixed(1)}L</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Anomalies */}
      {activeTab === 'anomalies' && anomalyData && (
        <div style={{ backgroundColor: '#FFFFFF', borderRadius: '8px', border: '1px solid #E2E8F0', overflow: 'hidden' }}>
          <div style={{ padding: '16px', borderBottom: '1px solid #E2E8F0' }}>
            <h3 style={{ margin: 0, fontSize: '15px', fontWeight: '700' }}>
              Detected Transaction & Operational Anomalies ({anomalyData.total_anomalies} total events)
            </h3>
          </div>
          <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {anomalyData.anomalies?.map((a: any, idx: number) => (
              <div key={idx} style={{ padding: '12px 16px', backgroundColor: a.severity === 'CRITICAL' ? '#FEF2F2' : '#F8FAFC', borderRadius: '6px', border: a.severity === 'CRITICAL' ? '1px solid #FCA5A5' : '1px solid #E2E8F0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <span style={{ fontWeight: '700', fontSize: '13px', color: '#0F172A' }}>{a.city} • {a.anomaly_type}</span>
                  <span style={{ fontSize: '11px', fontWeight: '700', color: a.severity === 'CRITICAL' ? '#B91C1C' : '#D97706' }}>
                    Severity: {a.severity} (Score: {a.anomaly_score})
                  </span>
                </div>
                <div style={{ fontSize: '12px', color: '#475569' }}>{a.reason}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState } from 'react';
import { api } from '../services/api';
import { UserRole } from '../types';

interface SqlAnalyticsViewProps {
  currentRole: UserRole;
}

export const SqlAnalyticsView: React.FC<SqlAnalyticsViewProps> = ({ currentRole }) => {
  const [prompt, setPrompt] = useState('Top 10 products by revenue');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const queryTemplates = [
    'Top 10 products by revenue',
    'Monthly revenue for Hyderabad branch',
    'High-risk churn customers with support tickets',
    'Inventory stock status and critical reorder items'
  ];

  const handleRun = async (selectedPrompt?: string) => {
    const q = selectedPrompt || prompt;
    setLoading(true);
    setError(null);
    try {
      const res = await api.executeSqlAnalytics(q);
      setResult(res);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Execution error');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#0F172A', margin: '0 0 6px 0' }}>
          Natural Language → SQL Analytics Engine
        </h2>
        <p style={{ fontSize: '13px', color: '#64748B', margin: 0 }}>
          Generates read-only SQL, strictly rejects mutations (DROP/DELETE/UPDATE/INSERT), and returns tabular data with chart inference.
        </p>
      </div>

      {/* Query Bar */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '16px' }}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask analytical question (e.g. 'Show top 10 products by revenue')..."
          style={{ flex: 1, padding: '12px 16px', borderRadius: '8px', border: '1px solid #CBD5E1', fontSize: '14px' }}
        />
        <button
          onClick={() => handleRun()}
          disabled={loading}
          style={{ backgroundColor: '#0284C7', color: '#FFFFFF', border: 'none', borderRadius: '8px', padding: '0 24px', fontWeight: '600', cursor: 'pointer' }}
        >
          {loading ? 'Executing...' : 'Run Query'}
        </button>
      </div>

      {/* Preset Templates */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        {queryTemplates.map((t, idx) => (
          <button
            key={idx}
            onClick={() => { setPrompt(t); handleRun(t); }}
            style={{ backgroundColor: '#F1F5F9', border: '1px solid #E2E8F0', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', color: '#334155', cursor: 'pointer' }}
          >
            📋 {t}
          </button>
        ))}
      </div>

      {error && (
        <div style={{ padding: '12px 16px', backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', color: '#B91C1C', borderRadius: '8px', marginBottom: '20px', fontSize: '13px' }}>
          ⚠️ {error}
        </div>
      )}

      {result && (
        <div>
          {/* SQL Code Block */}
          <div style={{ backgroundColor: '#0F172A', padding: '16px', borderRadius: '8px', marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94A3B8', fontSize: '11px', marginBottom: '8px' }}>
              <span>GENERATED SAFE SQL (READ-ONLY)</span>
              <span>⚡ Execution Time: {result.execution_time_ms} ms</span>
            </div>
            <pre style={{ margin: 0, color: '#38BDF8', fontFamily: 'JetBrains Mono, monospace', fontSize: '13px', overflowX: 'auto' }}>
              {result.sql}
            </pre>
          </div>

          {/* Results Table */}
          <div style={{ backgroundColor: '#FFFFFF', borderRadius: '8px', border: '1px solid #E2E8F0', overflow: 'hidden' }}>
            <div style={{ padding: '12px 16px', borderBottom: '1px solid #E2E8F0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: '600', fontSize: '13px' }}>Result Set ({result.total_rows} records)</span>
              {result.visualization && (
                <span style={{ fontSize: '12px', color: '#059669', backgroundColor: '#ECFDF5', padding: '3px 8px', borderRadius: '4px', border: '1px solid #A7F3D0' }}>
                  📊 Chart Type: {result.visualization.recommended_chart}
                </span>
              )}
            </div>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                <thead>
                  <tr style={{ backgroundColor: '#F8FAFC', borderBottom: '1px solid #E2E8F0' }}>
                    {result.columns.map((c: string, idx: number) => (
                      <th key={idx} style={{ padding: '10px 14px', color: '#475569', fontWeight: '600' }}>{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.rows.map((row: any, rIdx: number) => (
                    <tr key={rIdx} style={{ borderBottom: '1px solid #F1F5F9' }}>
                      {result.columns.map((c: string, cIdx: number) => (
                        <td key={cIdx} style={{ padding: '10px 14px', color: '#1E293B' }}>{String(row[c])}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

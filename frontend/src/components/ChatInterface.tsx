import React, { useState } from 'react';
import { api } from '../services/api';
import { ChatMessage, UserRole } from '../types';

interface ChatInterfaceProps {
  currentRole: UserRole;
  onWorkflowTriggered?: () => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ currentRole, onWorkflowTriggered }) => {
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'init-1',
      role: 'assistant',
      content: 'Welcome to the Enterprise AI Intelligence & Automation Platform. Ask anything about your organization, company documents, SQL analytics, ML predictions, or approved business workflows.',
      timestamp: 'Just now'
    }
  ]);

  const presetQueries = [
    'Why did our Hyderabad sales decline last month, which products were responsible, and what do you expect next month?',
    'Summarize our annual leave and sick policy.',
    'What were our top 10 products by revenue?',
    'Which customers are likely to churn?',
    'Predict next month\'s sales in Hyderabad.',
    'Create a monthly business report.',
    'Replenish IoT Gateway inventory in Hyderabad.'
  ];

  const handleSend = async (queryToSend?: string) => {
    const query = queryToSend || inputQuery;
    if (!query.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const res = await api.sendChatQuery(query);
      const assistantMsg: ChatMessage = {
        id: `res-${Date.now()}`,
        role: 'assistant',
        content: res.response,
        intent: res.intent,
        agent_selected: res.agent_selected,
        citations: res.citations || [],
        sql_query: res.sql_query,
        visualization: res.visualization,
        execution_time_ms: res.execution_time_ms,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (res.intent === 'WORKFLOW_ACTION' && onWorkflowTriggered) {
        onWorkflowTriggered();
      }
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `Error: ${err.response?.data?.detail || err.message || 'Failed to process request.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 70px)', maxWidth: '1200px', margin: '0 auto', padding: '16px' }}>
      {/* Preset Query Pills */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '12px', borderBottom: '1px solid #E2E8F0' }}>
        {presetQueries.map((pq, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(pq)}
            style={{
              whiteSpace: 'nowrap',
              backgroundColor: '#EFF6FF',
              color: '#1E40AF',
              border: '1px solid #BFDBFE',
              borderRadius: '16px',
              padding: '6px 12px',
              fontSize: '12px',
              cursor: 'pointer',
              fontWeight: '500',
              transition: 'all 0.2s'
            }}
          >
            💡 {pq.length > 55 ? pq.substring(0, 52) + '...' : pq}
          </button>
        ))}
      </div>

      {/* Messages Feed */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '20px 0', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {messages.map((m) => {
          const isUser = m.role === 'user';
          return (
            <div
              key={m.id}
              style={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
              }}
            >
              <div
                style={{
                  maxWidth: '82%',
                  backgroundColor: isUser ? '#1E40AF' : '#FFFFFF',
                  color: isUser ? '#FFFFFF' : '#1E293B',
                  borderRadius: '12px',
                  padding: '16px 20px',
                  boxShadow: isUser ? 'none' : '0 1px 3px rgba(0,0,0,0.1)',
                  border: isUser ? 'none' : '1px solid #E2E8F0',
                  lineHeight: '1.6',
                  fontSize: '14px'
                }}
              >
                {!isUser && m.agent_selected && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', borderBottom: '1px solid #F1F5F9', paddingBottom: '6px' }}>
                    <span style={{ backgroundColor: '#DBEAFE', color: '#1E40AF', fontSize: '11px', fontWeight: '700', padding: '2px 8px', borderRadius: '4px' }}>
                      {m.agent_selected}
                    </span>
                    {m.execution_time_ms && (
                      <span style={{ fontSize: '11px', color: '#64748B' }}>
                        ⚡ {m.execution_time_ms} ms
                      </span>
                    )}
                    {m.intent && (
                      <span style={{ fontSize: '11px', color: '#64748B' }}>
                        • Intent: {m.intent}
                      </span>
                    )}
                  </div>
                )}

                <div style={{ whiteSpace: 'pre-wrap' }}>{m.content}</div>

                {/* SQL Query Preview if executed */}
                {m.sql_query && (
                  <div style={{ marginTop: '12px', backgroundColor: '#0F172A', color: '#38BDF8', padding: '10px 14px', borderRadius: '6px', fontFamily: 'JetBrains Mono, monospace', fontSize: '12px' }}>
                    <div style={{ color: '#94A3B8', fontSize: '10px', textTransform: 'uppercase', marginBottom: '4px' }}>Validated Safe SQL:</div>
                    <code>{m.sql_query}</code>
                  </div>
                )}

                {/* Visualization Recommendation Badge */}
                {m.visualization && (
                  <div style={{ marginTop: '10px', display: 'flex', alignItems: 'center', gap: '6px', backgroundColor: '#F0FDF4', color: '#166534', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', border: '1px solid #BBF7D0' }}>
                    📈 Recommended Visualization: <b>{m.visualization.recommended_chart}</b> ({m.visualization.title})
                  </div>
                )}

                {/* Citations Preview */}
                {m.citations && m.citations.length > 0 && (
                  <div style={{ marginTop: '12px', paddingTop: '8px', borderTop: '1px solid #E2E8F0' }}>
                    <div style={{ fontSize: '11px', fontWeight: '700', color: '#475569', marginBottom: '4px' }}>
                      TRACEABLE CITATIONS:
                    </div>
                    {m.citations.map((c, i) => (
                      <div key={i} style={{ fontSize: '11px', color: '#0369A1', marginBottom: '2px' }}>
                        🔗 <b>{c.formatted_source}</b> (Document ID: {c.document_id})
                      </div>
                    ))}
                  </div>
                )}

                <div style={{ fontSize: '10px', color: isUser ? '#93C5FD' : '#94A3B8', textAlign: 'right', marginTop: '6px' }}>
                  {m.timestamp}
                </div>
              </div>
            </div>
          );
        })}

        {loading && (
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', color: '#64748B', fontSize: '13px' }}>
            <span style={{ animation: 'spin 1s linear infinite' }}>⏳</span>
            AI Orchestrator is classifying intent and coordinating sub-agents...
          </div>
        )}
      </div>

      {/* Query Input Box */}
      <div style={{ display: 'flex', gap: '10px', paddingTop: '12px', borderTop: '1px solid #E2E8F0' }}>
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={`Ask anything about company data, policies, or predictions (as ${currentRole})...`}
          style={{
            flex: 1,
            padding: '14px 18px',
            fontSize: '14px',
            border: '1px solid #CBD5E1',
            borderRadius: '8px',
            outline: 'none'
          }}
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !inputQuery.trim()}
          style={{
            backgroundColor: loading || !inputQuery.trim() ? '#94A3B8' : '#2563EB',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: '8px',
            padding: '0 24px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: loading || !inputQuery.trim() ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </div>
  );
};

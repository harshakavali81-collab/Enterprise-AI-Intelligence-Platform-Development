import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { WorkflowTicket, UserRole } from '../types';

interface WorkflowApprovalModalProps {
  currentRole: UserRole;
  onDecisionSubmitted?: () => void;
}

export const WorkflowApprovalModal: React.FC<WorkflowApprovalModalProps> = ({ currentRole, onDecisionSubmitted }) => {
  const [workflows, setWorkflows] = useState<WorkflowTicket[]>([]);
  const [loading, setLoading] = useState(false);
  const [decisionFeedback, setDecisionFeedback] = useState<string | null>(null);

  const fetchWorkflows = async () => {
    setLoading(true);
    try {
      const data = await api.getPendingWorkflows();
      setWorkflows(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkflows();
  }, []);

  const handleDecision = async (id: number, decision: 'APPROVE' | 'REJECT') => {
    try {
      const res = await api.submitWorkflowDecision(id, decision);
      setDecisionFeedback(res.message);
      fetchWorkflows();
      if (onDecisionSubmitted) onDecisionSubmitted();
    } catch (err: any) {
      setDecisionFeedback(`Failed: ${err.response?.data?.detail || err.message}`);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#0F172A', margin: '0 0 6px 0' }}>
          Human-In-The-Loop (HITL) Workflow Governance
        </h2>
        <p style={{ fontSize: '13px', color: '#64748B', margin: 0 }}>
          High-impact automated actions (inventory orders, client interventions, report dispatches) require policy review and managerial authorization.
        </p>
      </div>

      {decisionFeedback && (
        <div style={{ padding: '12px 16px', backgroundColor: '#F0FDF4', border: '1px solid #BBF7D0', color: '#166534', borderRadius: '8px', marginBottom: '16px', fontSize: '13px' }}>
          ✅ {decisionFeedback}
        </div>
      )}

      {loading && <div style={{ color: '#64748B', fontSize: '14px' }}>Loading pending workflows...</div>}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {workflows.length === 0 && !loading && (
          <div style={{ backgroundColor: '#FFFFFF', padding: '32px', borderRadius: '8px', textAlign: 'center', color: '#64748B', border: '1px solid #E2E8F0' }}>
            🎉 No pending approval tickets. All enterprise workflows are up to date!
          </div>
        )}

        {workflows.map((wf) => (
          <div key={wf.workflow_id} style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '8px', border: '1px solid #E2E8F0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
              <div>
                <span style={{ fontSize: '11px', fontWeight: '700', color: '#D97706', backgroundColor: '#FEF3C7', padding: '3px 8px', borderRadius: '4px', textTransform: 'uppercase' }}>
                  {wf.status.replace('_', ' ')}
                </span>
                <h3 style={{ margin: '8px 0 4px 0', fontSize: '16px', fontWeight: '700', color: '#0F172A' }}>
                  #{wf.workflow_id}: {wf.title}
                </h3>
              </div>
              <span style={{ fontSize: '12px', color: '#64748B' }}>Created: {wf.created_at}</span>
            </div>

            <p style={{ fontSize: '13px', color: '#334155', lineHeight: '1.5', margin: '0 0 12px 0' }}>
              {wf.description}
            </p>

            <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#64748B', marginBottom: '16px', borderTop: '1px solid #F1F5F9', paddingTop: '10px' }}>
              <span><b>Triggered By:</b> {wf.triggered_by}</span>
              <span><b>Impact Level:</b> {wf.impact_level}</span>
              <span><b>Required Sign-off:</b> {wf.approver_role}</span>
            </div>

            <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => handleDecision(wf.workflow_id, 'REJECT')}
                disabled={currentRole === 'EMPLOYEE'}
                style={{
                  backgroundColor: '#FFFFFF',
                  color: '#DC2626',
                  border: '1px solid #FCA5A5',
                  borderRadius: '6px',
                  padding: '8px 18px',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: currentRole === 'EMPLOYEE' ? 'not-allowed' : 'pointer'
                }}
              >
                Reject Action
              </button>
              <button
                onClick={() => handleDecision(wf.workflow_id, 'APPROVE')}
                disabled={currentRole === 'EMPLOYEE'}
                style={{
                  backgroundColor: currentRole === 'EMPLOYEE' ? '#94A3B8' : '#16A34A',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '8px 22px',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: currentRole === 'EMPLOYEE' ? 'not-allowed' : 'pointer'
                }}
              >
                {currentRole === 'EMPLOYEE' ? 'Requires Manager Role' : 'Approve & Execute'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

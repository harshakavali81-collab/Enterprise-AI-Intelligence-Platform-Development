import React from 'react';
import { UserRole } from '../types';

interface NavbarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  currentRole: UserRole;
  setCurrentRole: (role: UserRole) => void;
  pendingApprovalsCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  setCurrentTab,
  currentRole,
  setCurrentRole,
  pendingApprovalsCount
}) => {
  const tabs = [
    { id: 'chat', label: 'AI Intelligence Hub', icon: '🤖' },
    { id: 'documents', label: 'Document RAG', icon: '📄' },
    { id: 'analytics', label: 'SQL Analytics', icon: '📊' },
    { id: 'ml', label: 'Predictive ML Engine', icon: '📈' },
    { id: 'workflows', label: `Workflows (${pendingApprovalsCount})`, icon: '⚡' },
  ];

  return (
    <header style={{
      backgroundColor: '#0F172A',
      color: '#FFFFFF',
      padding: '12px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottom: '1px solid #334155',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 'bold',
          fontSize: '18px'
        }}>
          AI
        </div>
        <div>
          <h1 style={{ margin: 0, fontSize: '18px', fontWeight: '700', letterSpacing: '-0.3px' }}>
            ENTERPRISE AI INTELLIGENCE PLATFORM
          </h1>
          <span style={{ fontSize: '11px', color: '#94A3B8' }}>
            Production RAG • Multi-Agent • SQL • Predictive ML • Workflows
          </span>
        </div>
      </div>

      <nav style={{ display: 'flex', gap: '8px' }}>
        {tabs.map((tab) => {
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setCurrentTab(tab.id)}
              style={{
                backgroundColor: isActive ? '#1E293B' : 'transparent',
                color: isActive ? '#38BDF8' : '#CBD5E1',
                border: isActive ? '1px solid #38BDF8' : '1px solid transparent',
                borderRadius: '6px',
                padding: '8px 14px',
                fontSize: '13px',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.2s'
              }}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          );
        })}
      </nav>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontSize: '12px', color: '#94A3B8' }}>Active Role:</span>
        <select
          value={currentRole}
          onChange={(e) => setCurrentRole(e.target.value as UserRole)}
          style={{
            backgroundColor: '#1E293B',
            color: '#F8FAFC',
            border: '1px solid #475569',
            borderRadius: '6px',
            padding: '6px 12px',
            fontSize: '12px',
            fontWeight: '600',
            cursor: 'pointer'
          }}
        >
          <option value="ADMIN">ADMIN (Superuser)</option>
          <option value="MANAGER">MANAGER (Approver / Reports)</option>
          <option value="ANALYST">ANALYST (SQL & ML)</option>
          <option value="EMPLOYEE">EMPLOYEE (Document RAG)</option>
        </select>
      </div>
    </header>
  );
};

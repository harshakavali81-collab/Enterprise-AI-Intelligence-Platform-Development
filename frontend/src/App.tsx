import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { ChatInterface } from './components/ChatInterface';
import { DocumentManager } from './components/DocumentManager';
import { SqlAnalyticsView } from './components/SqlAnalyticsView';
import { MlPredictionsView } from './components/MlPredictionsView';
import { WorkflowApprovalModal } from './components/WorkflowApprovalModal';
import { UserRole } from './types';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<string>('chat');
  const [currentRole, setCurrentRole] = useState<UserRole>('MANAGER');
  const [pendingApprovalsCount, setPendingApprovalsCount] = useState<number>(2);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#F8FAFC', display: 'flex', flexDirection: 'column' }}>
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        currentRole={currentRole}
        setCurrentRole={setCurrentRole}
        pendingApprovalsCount={pendingApprovalsCount}
      />

      <main style={{ flex: 1 }}>
        {currentTab === 'chat' && (
          <ChatInterface
            currentRole={currentRole}
            onWorkflowTriggered={() => setPendingApprovalsCount((c) => c + 1)}
          />
        )}
        {currentTab === 'documents' && <DocumentManager currentRole={currentRole} />}
        {currentTab === 'analytics' && <SqlAnalyticsView currentRole={currentRole} />}
        {currentTab === 'ml' && <MlPredictionsView />}
        {currentTab === 'workflows' && (
          <WorkflowApprovalModal
            currentRole={currentRole}
            onDecisionSubmitted={() => setPendingApprovalsCount((c) => Math.max(0, c - 1))}
          />
        )}
      </main>
    </div>
  );
};

export default App;

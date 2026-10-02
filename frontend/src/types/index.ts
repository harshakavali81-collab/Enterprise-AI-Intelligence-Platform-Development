export type UserRole = 'ADMIN' | 'MANAGER' | 'ANALYST' | 'EMPLOYEE';

export interface User {
  user_id: number;
  username: string;
  full_name: string;
  email: string;
  role: UserRole;
  department: string;
}

export interface Citation {
  citation_id: string;
  document_title: string;
  document_id: string;
  page_number: number;
  section: string;
  formatted_source: string;
  snippet: string;
}

export interface VisualizationConfig {
  recommended_chart: 'LINE_CHART' | 'BAR_CHART' | 'DONUT_CHART' | 'TABLE';
  title?: string;
  x_axis?: string;
  y_axis?: string;
  dimension?: string;
  metric?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  agent_selected?: string;
  citations?: Citation[];
  sql_query?: string;
  visualization?: VisualizationConfig;
  execution_time_ms?: number;
  timestamp: string;
}

export interface WorkflowTicket {
  workflow_id: number;
  workflow_type: string;
  title: string;
  description: string;
  triggered_by: string;
  impact_level: string;
  status: 'PENDING_APPROVAL' | 'APPROVED_AND_EXECUTED' | 'REJECTED';
  approver_role: string;
  created_at: string;
}

export interface DocumentMeta {
  document_id: string;
  title: string;
  filename: string;
  department: string;
  category: string;
  access_level: UserRole;
}

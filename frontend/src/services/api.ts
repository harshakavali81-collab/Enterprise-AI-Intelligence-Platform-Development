import axios from 'axios';
import { User, ChatMessage, WorkflowTicket, DocumentMeta } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Authentication
  login: async (username: string, password: string) => {
    const res = await client.post('/auth/login', { username, password });
    return res.data;
  },

  // AI Chat & Multi-Agent Orchestrator
  sendChatQuery: async (query: string, token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.post('/chat', { query }, { headers });
    return res.data;
  },

  // SQL & Analytics
  executeSqlAnalytics: async (prompt: string, token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.post('/analytics/sql', { prompt }, { headers });
    return res.data;
  },

  getKpis: async (token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.get('/analytics/kpis', { headers });
    return res.data;
  },

  // Predictive ML
  predictChurn: async (customerData?: any, token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.post('/predict/churn', customerData || {}, { headers });
    return res.data;
  },

  predictForecast: async (city: string = 'Hyderabad', token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.post('/predict/forecast', { city }, { headers });
    return res.data;
  },

  getAnomalies: async (token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.get('/predict/anomalies', { headers });
    return res.data;
  },

  // Documents
  getDocuments: async (token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.get('/documents', { headers });
    return res.data;
  },

  // Workflows & Approvals
  getPendingWorkflows: async (token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.get('/workflows/pending', { headers });
    return res.data;
  },

  submitWorkflowDecision: async (workflow_id: number, decision: 'APPROVE' | 'REJECT', token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.post('/workflows/decision', { workflow_id, decision }, { headers });
    return res.data;
  },

  // Reports
  generateReport: async (title: string, token?: string) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await client.post('/reports/generate', { title, format: 'PDF' }, { headers });
    return res.data;
  }
};

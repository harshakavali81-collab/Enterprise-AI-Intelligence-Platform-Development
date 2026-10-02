import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { DocumentMeta, UserRole } from '../types';

interface DocumentManagerProps {
  currentRole: UserRole;
}

export const DocumentManager: React.FC<DocumentManagerProps> = ({ currentRole }) => {
  const [docs, setDocs] = useState<DocumentMeta[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getDocuments().then(setDocs).catch(console.error);
  }, []);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    try {
      const res = await api.sendChatQuery(searchQuery);
      setSearchResult(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#0F172A', margin: '0 0 6px 0' }}>
          Document Intelligence & RAG Knowledge Repository
        </h2>
        <p style={{ fontSize: '13px', color: '#64748B', margin: 0 }}>
          Ingests multi-format policies, SOPs, and reports. Employs semantic chunking, 768-dim embeddings, and hybrid retrieval with metadata RBAC filtering.
        </p>
      </div>

      {/* Semantic Search Box */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '24px' }}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Semantic search policies & SOPs (e.g. 'What is the sick leave policy?')..."
          style={{ flex: 1, padding: '12px 16px', borderRadius: '8px', border: '1px solid #CBD5E1', fontSize: '14px' }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{ backgroundColor: '#2563EB', color: '#FFFFFF', border: 'none', borderRadius: '8px', padding: '0 24px', fontWeight: '600', cursor: 'pointer' }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {/* Grounded Search Result with Citations */}
      {searchResult && (
        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '8px', border: '1px solid #E2E8F0', marginBottom: '24px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
          <div style={{ fontSize: '12px', color: '#1E40AF', fontWeight: '700', marginBottom: '8px' }}>
            GROUNDED RAG RESPONSE
          </div>
          <div style={{ fontSize: '14px', lineHeight: '1.6', color: '#1E293B', whiteSpace: 'pre-wrap' }}>
            {searchResult.response}
          </div>
        </div>
      )}

      {/* Ingested Documents Grid */}
      <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#0F172A', marginBottom: '12px' }}>
        Ingested Knowledge Documents ({docs.length})
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
        {docs.map((doc, idx) => (
          <div key={idx} style={{ backgroundColor: '#FFFFFF', padding: '16px', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
              <span style={{ fontSize: '24px' }}>📄</span>
              <span style={{ backgroundColor: '#F1F5F9', color: '#475569', fontSize: '11px', fontWeight: '600', padding: '2px 8px', borderRadius: '4px' }}>
                {doc.access_level}
              </span>
            </div>
            <div style={{ fontWeight: '700', fontSize: '14px', color: '#0F172A', marginBottom: '4px' }}>
              {doc.title}
            </div>
            <div style={{ fontSize: '12px', color: '#64748B', marginBottom: '8px' }}>
              <b>Dept:</b> {doc.department} • <b>Category:</b> {doc.category}
            </div>
            <div style={{ fontSize: '11px', color: '#94A3B8', fontFamily: 'JetBrains Mono, monospace' }}>
              File: {doc.filename}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

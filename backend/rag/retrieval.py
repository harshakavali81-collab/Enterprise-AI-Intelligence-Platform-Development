import re, math
from typing import List, Dict, Any, Optional
from backend.rag.embeddings import EmbeddingService

class HybridRetrievalEngine:
    """
    Hybrid Search Engine combining Dense Vector Search, BM25 Lexical Matching,
    and Enterprise Metadata/RBAC Filtering.
    """
    def __init__(self, embedding_service: Optional[EmbeddingService] = None, alpha: float = 0.65):
        self.embedding_service = embedding_service or EmbeddingService()
        self.alpha = alpha # 0.65 dense vector weight, 0.35 lexical weight

    def search(
        self,
        query: str,
        corpus_chunks: List[Dict[str, Any]],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        user_role: str = "EMPLOYEE"
    ) -> List[Dict[str, Any]]:
        if not corpus_chunks or not query:
            return []

        # 1. RBAC & Metadata Filtering
        role_hierarchy = {"EMPLOYEE": 1, "ANALYST": 2, "MANAGER": 3, "ADMIN": 4}
        user_rank = role_hierarchy.get(user_role.upper(), 1)

        filtered_chunks = []
        for chunk in corpus_chunks:
            meta = chunk.get("metadata", {})
            required_role = meta.get("access_level", "EMPLOYEE").upper()
            if role_hierarchy.get(required_role, 1) > user_rank:
                continue # Skip chunks above user's clearance

            # Apply explicit attribute filters
            if filters:
                match = True
                for f_key, f_val in filters.items():
                    if f_val and meta.get(f_key, "").lower() != str(f_val).lower():
                        match = False
                        break
                if not match:
                    continue

            filtered_chunks.append(chunk)

        if not filtered_chunks:
            return []

        # 2. Dense Vector Scoring
        q_vec = self.embedding_service.get_embedding(query)
        for chunk in filtered_chunks:
            c_vec = chunk.get("embedding")
            if not c_vec:
                c_vec = self.embedding_service.get_embedding(chunk["content"])
                chunk["embedding"] = c_vec
            chunk["vector_score"] = self.embedding_service.compute_similarity(q_vec, c_vec)

        # 3. Lexical / Keyword Scoring (BM25 Approximation)
        q_terms = set(re.findall(r"\w+", query.lower()))
        for chunk in filtered_chunks:
            c_text = chunk["content"].lower()
            term_matches = sum(1 for term in q_terms if term in c_text)
            chunk["keyword_score"] = term_matches / max(len(q_terms), 1)

        # 4. Hybrid Fusion (Score = alpha * Vector + (1-alpha) * Lexical)
        for chunk in filtered_chunks:
            chunk["hybrid_score"] = round(
                self.alpha * chunk["vector_score"] + (1 - self.alpha) * chunk["keyword_score"],
                4
            )

        ranked = sorted(filtered_chunks, key=lambda x: x["hybrid_score"], reverse=True)
        return ranked[:top_k]

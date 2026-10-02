import re
from typing import List, Dict, Any

class ContextualReranker:
    """
    Cross-Encoder / Contextual Reranking Service.
    Re-scores top retrieved chunks by assessing semantic density,
    exact entity/numeric matches, and title relevance.
    """
    def rerank(self, query: str, retrieved_chunks: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        if not retrieved_chunks:
            return []

        q_lower = query.lower()
        q_tokens = set(re.findall(r"\w+", q_lower))

        for chunk in retrieved_chunks:
            base_score = chunk.get("hybrid_score", 0.5)
            content = chunk["content"].lower()
            meta = chunk.get("metadata", {})
            title = meta.get("title", "").lower()

            boost = 0.0
            # Exact title or category match
            if any(token in title for token in q_tokens if len(token) > 3):
                boost += 0.15

            # Numerical or currency queries (e.g. ₹, limit, days, percent)
            if any(char in q_lower for char in ["₹", "rs", "limit", "day", "percent", "%", "allowance"]):
                if any(char in content for char in ["₹", "rs", "days", "allowance", "limit", "%"]):
                    boost += 0.20

            # Exact consecutive 2-word phrase overlap
            words = list(q_tokens)
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                if phrase in content:
                    boost += 0.10

            chunk["rerank_score"] = round(min(base_score + boost, 1.0), 4)

        reranked = sorted(retrieved_chunks, key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_n]

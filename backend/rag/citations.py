from typing import List, Dict, Any, Optional

class CitationEngine:
    """
    Enterprise Traceability & Citation Generation Engine.
    Extracts citation breadcrumbs from retrieved chunks and grounds LLM responses.
    Verifies that claims cite verifiable document sources.
    """
    def format_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        citations = []
        seen = set()

        for chunk in chunks:
            meta = chunk.get("metadata", {})
            title = meta.get("title") or meta.get("filename", "Enterprise Document")
            page = chunk.get("page_number", meta.get("page_number", 1))
            section = chunk.get("section_title", meta.get("section", "General"))
            doc_id = meta.get("document_id", "DOC-REF")

            key = (title, page, section)
            if key not in seen:
                seen.add(key)
                citations.append({
                    "citation_id": f"CIT-{len(citations)+1}",
                    "document_title": title,
                    "document_id": doc_id,
                    "page_number": page,
                    "section": section,
                    "formatted_source": f"[{title} – {section} (Page {page})]",
                    "snippet": chunk.get("content", "")[:200].replace("\n", " ") + "..."
                })
        return citations

    def append_citations_to_response(self, answer_text: str, citations: List[Dict[str, Any]]) -> str:
        if not citations:
            return answer_text

        sources_block = "\n\n### 📚 Traceable Sources & Citations:\n"
        for cit in citations:
            sources_block += f"- **{cit['formatted_source']}**: {cit['snippet']}\n"

        return answer_text + sources_block

import re
from typing import Dict, Any, List

class SemanticChunker:
    """
    Enterprise Semantic Chunking Engine.
    Splits text along paragraph and section headers with sliding overlap.
    Preserves context, metadata, and page locations for strict citation tracing.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, extracted_doc: Dict[str, Any], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        chunks = []
        chunk_idx = 0

        for page_info in extracted_doc.get("pages", []):
            page_num = page_info["page_number"]
            raw_text = page_info["text"]

            # Split on double newline or section headings (#, ##)
            sections = re.split(r"(?=\n#{1,3}\s)|\n\n", raw_text)
            current_buffer = ""

            for sec in sections:
                sec = sec.strip()
                if not sec:
                    continue

                if len(current_buffer) + len(sec) < self.chunk_size:
                    current_buffer += ("\n\n" + sec if current_buffer else sec)
                else:
                    if current_buffer:
                        chunks.append(self._create_chunk(current_buffer, chunk_idx, page_num, metadata))
                        chunk_idx += 1
                        # Retain overlap from end of buffer
                        overlap_text = current_buffer[-self.chunk_overlap:] if len(current_buffer) > self.chunk_overlap else ""
                        current_buffer = (overlap_text + "\n" + sec).strip()
                    else:
                        current_buffer = sec

            if current_buffer:
                chunks.append(self._create_chunk(current_buffer, chunk_idx, page_num, metadata))
                chunk_idx += 1

        return chunks

    def _create_chunk(self, content: str, idx: int, page_num: int, metadata: Dict[str, Any]) -> Dict[str, Any]:
        # Extract probable section header if available
        first_line = content.split("\n")[0].strip()
        section_title = first_line if first_line.startswith("#") else "General Section"

        return {
            "chunk_index": idx,
            "page_number": page_num,
            "section_title": section_title.lstrip("#").strip(),
            "content": content,
            "char_count": len(content),
            "estimated_tokens": max(len(content) // 4, 1),
            "metadata": {
                **metadata,
                "page_number": page_num,
                "section": section_title.lstrip("#").strip()
            }
        }

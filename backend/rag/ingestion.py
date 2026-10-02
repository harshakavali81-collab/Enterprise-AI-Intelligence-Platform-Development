import os, re
from typing import Dict, Any, List, Optional
import pypdf
import docx
import openpyxl

class DocumentIngestionService:
    """
    Production Document Ingestion & Text Extraction Service.
    Supports multi-format parsing: PDF, DOCX, TXT, CSV, XLSX, Markdown.
    Extracts structured metadata, sanitizes text, and prepares documents for chunking.
    """
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"}

    def validate_file(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{ext}'. Supported: {self.SUPPORTED_EXTENSIONS}")
        return True

    def extract_text(self, file_path: str) -> Dict[str, Any]:
        self.validate_file(file_path)
        ext = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path)
        pages_content = []

        if ext in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                pages_content.append({"page_number": 1, "text": content})

        elif ext == ".pdf":
            try:
                reader = pypdf.PdfReader(file_path)
                for idx, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    pages_content.append({"page_number": idx + 1, "text": text})
            except Exception as e:
                # Fallback to plain read if PDF parser encounters raw stream
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    pages_content.append({"page_number": 1, "text": f.read()})

        elif ext == ".docx":
            doc = docx.Document(file_path)
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            pages_content.append({"page_number": 1, "text": full_text})

        elif ext == ".xlsx":
            wb = openpyxl.load_workbook(file_path, data_only=True)
            text_lines = []
            for sheetname in wb.sheetnames:
                ws = wb[sheetname]
                text_lines.append(f"--- Sheet: {sheetname} ---")
                for row in ws.iter_rows(values_only=True):
                    row_vals = [str(c) for c in row if c is not None]
                    if row_vals:
                        text_lines.append(" | ".join(row_vals))
            pages_content.append({"page_number": 1, "text": "\n".join(text_lines)})

        elif ext == ".csv":
            import pandas as pd
            df = pd.read_csv(file_path)
            summary_text = f"CSV Table with {len(df)} rows and columns: {list(df.columns)}\n"
            summary_text += df.head(50).to_string()
            pages_content.append({"page_number": 1, "text": summary_text})

        # Text cleaning & normalization
        for item in pages_content:
            text = item["text"]
            # Clean repetitive whitespace, non-printable characters
            text = re.sub(r"\r\n", "\n", text)
            text = re.sub(r"[ \t]+", " ", text)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            item["text"] = text

        return {
            "filename": filename,
            "file_type": ext.lstrip("."),
            "file_size_bytes": os.path.getsize(file_path),
            "pages": pages_content,
            "total_pages": len(pages_content)
        }

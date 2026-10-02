import unittest
from backend.rag.ingestion import DocumentIngestionService
from backend.rag.chunking import SemanticChunker
from backend.rag.embeddings import EmbeddingService
from backend.rag.retrieval import HybridRetrievalEngine
from backend.rag.citations import CitationEngine

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.ingestion = DocumentIngestionService()
        self.chunker = SemanticChunker(chunk_size=300, chunk_overlap=50)
        self.embedding = EmbeddingService(dimension=768)
        self.retrieval = HybridRetrievalEngine(self.embedding)
        self.citations = CitationEngine()

    def test_document_extraction(self):
        sample_doc = "data/sample/hr_policy.txt"
        extracted = self.ingestion.extract_text(sample_doc)
        self.assertEqual(extracted["filename"], "hr_policy.txt")
        self.assertGreater(len(extracted["pages"]), 0)
        self.assertIn("leave", extracted["pages"][0]["text"].lower())

    def test_chunking(self):
        doc = {
            "filename": "test.txt",
            "pages": [{"page_number": 1, "text": "# Section A\nThis is paragraph one.\n\n# Section B\nThis is paragraph two."}]
        }
        meta = {"title": "Test Doc", "access_level": "EMPLOYEE"}
        chunks = self.chunker.chunk_document(doc, meta)
        self.assertGreaterEqual(len(chunks), 1)
        self.assertIn("Section", chunks[0]["section_title"])

    def test_embedding_normalization(self):
        vec = self.embedding.get_embedding("Enterprise AI RAG system")
        self.assertEqual(len(vec), 768)
        import numpy as np
        norm = np.linalg.norm(vec)
        self.assertAlmostEqual(norm, 1.0, places=3)

    def test_hybrid_search_and_rbac(self):
        corpus = [
            {
                "content": "Employee leave policy allows 24 days annual vacation.",
                "metadata": {"title": "HR Policy", "access_level": "EMPLOYEE", "page_number": 1}
            },
            {
                "content": "Executive board secret compensation details.",
                "metadata": {"title": "Board Review", "access_level": "ADMIN", "page_number": 1}
            }
        ]
        # Employee should only see Employee clearance documents
        results_emp = self.retrieval.search("leave policy", corpus, user_role="EMPLOYEE")
        self.assertGreaterEqual(len(results_emp), 1)
        self.assertTrue(all(r["metadata"]["access_level"] == "EMPLOYEE" for r in results_emp))
        self.assertFalse(any("compensation" in r["content"] for r in results_emp))

        # Admin can access ADMIN clearance documents
        results_admin = self.retrieval.search("compensation", corpus, user_role="ADMIN")
        self.assertGreaterEqual(len(results_admin), 1)
        self.assertTrue(any("compensation" in r["content"] for r in results_admin))

    def test_citations(self):
        chunks = [{
            "content": "The reimbursement limit is 6500 per night for hotels.",
            "metadata": {"title": "Expense Policy", "document_id": "DOC-FIN-004", "page_number": 2, "section": "Travel"}
        }]
        cits = self.citations.format_citations(chunks)
        self.assertEqual(len(cits), 1)
        self.assertIn("Expense Policy", cits[0]["formatted_source"])
        self.assertEqual(cits[0]["page_number"], 2)

if __name__ == "__main__":
    unittest.main()

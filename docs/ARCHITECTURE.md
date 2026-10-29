# AI Disaster Response and Public Safety Assistant — architecture

**User / need:** Residents and disaster preparedness educators. Finding preparedness instructions without mistaking generated claims for official active warnings.

**Inputs:** `sample_request.json`; JSON validated by FastAPI and the domain engine.

**Domain method:** Synthetic-document TF-IDF retrieval with citations and abstention, prepared for future approved multilingual embeddings and official alert adapters.

**Pipeline:** User input → API checks → Multilingual RAG → structured evidence, caveats, or human-review flag → client.

**Trust boundary:** Live feeds are not connected; all knowledge files are fictional and all real-world inferences are hypothetical.

**Run:** `python projects/ai-disaster-response-public-safety-assistant/cli.py` after installing `requirements.txt` from project collection root.

```mermaid
flowchart LR
  A[User or synthetic fixture] --> B[FastAPI validation]
  B --> C[Multilingual RAG]
  C --> D[Provenance and limitations]
  D --> E[Human-reviewed result]
```

For a regulated release: perform an approved data-source ingestion design, versioned models, a durable store, rate limits and access control, auditability, monitoring and independent expert review.

# Emergency Services Information and Coordination Copilot — architecture

**User / need:** Authorized staff performing training exercises. Finding the right SOP text and drafting a report without making unauthorized operational changes.

**Inputs:** `sample_request.json`; JSON validated by FastAPI and the domain engine.

**Domain method:** Synthetic SOP retrieval, source citation and evidence-preserving draft; no tools execute dispatch or resource allocation.

**Pipeline:** User input → API checks → Procedure RAG → structured evidence, caveats, or human-review flag → client.

**Trust boundary:** Live feeds are not connected; all knowledge files are fictional and all real-world inferences are hypothetical.

**Run:** `python projects/emergency-services-coordination-copilot/cli.py` after installing `requirements.txt` from project collection root.

```mermaid
flowchart LR
  A[User or synthetic fixture] --> B[FastAPI validation]
  B --> C[Procedure RAG]
  C --> D[Provenance and limitations]
  D --> E[Human-reviewed result]
```

For a regulated release: perform an approved data-source ingestion design, versioned models, a durable store, rate limits and access control, auditability, monitoring and independent expert review.

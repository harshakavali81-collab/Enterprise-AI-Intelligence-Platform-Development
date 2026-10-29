# AI Flood and Natural Disaster Early-Warning Support — architecture

**User / need:** Researchers and disaster preparedness teams. Studying temporal trends while keeping statistical estimates separate from official forecasts.

**Inputs:** `sample_request.json`; JSON validated by FastAPI and the domain engine.

**Domain method:** Lagged Ridge model with chronological MAE vs persistence baseline, using only synthetic fixture or uploaded numerical series.

**Pipeline:** User input → API checks → Time-series regression → structured evidence, caveats, or human-review flag → client.

**Trust boundary:** Live feeds are not connected; all knowledge files are fictional and all real-world inferences are hypothetical.

**Run:** `python projects/ai-flood-disaster-early-warning/cli.py` after installing `requirements.txt` from project collection root.

```mermaid
flowchart LR
  A[User or synthetic fixture] --> B[FastAPI validation]
  B --> C[Time-series regression]
  C --> D[Provenance and limitations]
  D --> E[Human-reviewed result]
```

For a regulated release: perform an approved data-source ingestion design, versioned models, a durable store, rate limits and access control, auditability, monitoring and independent expert review.

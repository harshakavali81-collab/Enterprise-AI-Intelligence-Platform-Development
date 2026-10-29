# Privacy-Preserving Missing-Person Information Coordination — architecture

**User / need:** Authorized organizations conducting synthetic case-review exercises. Reducing duplicate intake while protecting sensitive records and preventing false identity matches.

**Inputs:** `sample_request.json`; JSON validated by FastAPI and the domain engine.

**Domain method:** Difflib sequence similarity for fictional tags with opaque reference codes; never merge a case or recognize faces.

**Pipeline:** User input → API checks → Pseudonymous similarity → structured evidence, caveats, or human-review flag → client.

**Trust boundary:** Live feeds are not connected; all knowledge files are fictional and all real-world inferences are hypothetical.

**Run:** `python projects/privacy-preserving-missing-person-coordination/cli.py` after installing `requirements.txt` from project collection root.

```mermaid
flowchart LR
  A[User or synthetic fixture] --> B[FastAPI validation]
  B --> C[Pseudonymous similarity]
  C --> D[Provenance and limitations]
  D --> E[Human-reviewed result]
```

For a regulated release: perform an approved data-source ingestion design, versioned models, a durable store, rate limits and access control, auditability, monitoring and independent expert review.

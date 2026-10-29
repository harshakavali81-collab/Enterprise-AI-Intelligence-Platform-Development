# Architecture and boundaries

```mermaid
flowchart LR
  U[User demo input] --> API[FastAPI gateway]
  API --> S{Select 1 of 10 modules}
  S --> R[TF-IDF source retrieval]
  S --> F[Chronological Ridge forecast]
  S --> C[TF-IDF Logistic Regression]
  S --> G[Spatial grid and case similarity]
  R --> P[Provenance and abstention]
  F --> P
  C --> P
  G --> P
  P --> O[Structured JSON response + limitations]
```

No live external fetch, remote LLM, real-time alerts, face recognition, autonomous dispatch, medical diagnosis or government eligibility decisions. The model selection is deliberately conservative and explicitly described by project. SQLite/PostgreSQL, OAuth, monitoring and signed provenance must be added with security review before operational deployment.

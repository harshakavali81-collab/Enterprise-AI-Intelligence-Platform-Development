# Privacy-Preserving Missing-Person Information Coordination

![Original project cover](assets/cover.svg)

> **Status:** Demonstration-grade source code using synthetic examples; no real operational deployment, authorized live feed, or independently verified field impact.

**Public need / intended users:** Reducing duplicate intake while protecting sensitive records and preventing false identity matches. **Audience:** Authorized organizations conducting synthetic case-review exercises.

**Technical evidence:** Pseudonymous similarity • privacy • human decisions. Difflib sequence similarity for fictional tags with opaque reference codes; never merge a case or recognize faces.

## Reproducible setup

Start at `public-benefit-ai/`:

```bash
pip install -r requirements.txt
python projects/privacy-preserving-missing-person-coordination/cli.py
uvicorn app.main:app --reload
pytest -q
python -m scripts.evaluate
```

**API endpoint:** `POST /api/v1/privacy-preserving-missing-person-coordination/analyze`

**Example payload:** [sample_request.json](sample_request.json). The FastAPI interactive schema is at `http://127.0.0.1:8000/docs`.

## Architecture, graphics and reproducibility

![Architecture illustration](assets/architecture.svg)

![Illustrative, fictional-data graphic](assets/synthetic-trend.svg)

- [Workflow source](docs/workflow.mmd) and [detailed architecture](docs/ARCHITECTURE.md).
- [Model card and evaluation plan](docs/MODEL_CARD.md), [threat model](docs/THREAT_MODEL.md).
- Synthetic fixture: `sample_request.json`; run in `cli.py`.
- Shared service: `../../app/` (model and routing implementation), `../../tests/` (automated checks), `../../Dockerfile`, and `../../scripts/evaluate.py`.
- Frontend dashboard: `../../frontend/index.html`; this requires the API server to function.

## Dataset / source trust

**Planned authorized sources:** Only separately authorized case records (NOT connected or public). Demonstration data is fabricated; no source licensing or source freshness has been verified through a real ingest.

## Evaluation: do not fabricate results

**Measure:** Labeled-pair precision/recall, false-match rate, audit trace completeness. The shared forecast modules report baseline and model MAE on chronological holdout when enough observations are provided. Running the evaluation script computes a small synthetic retrieval smoke test. Neither proves live field accuracy.

## Responsible AI constraints

No public person search, no publication of identities or face recognition. Report uncertainty and require human approval for consequential decisions.

**Not yet complete:** licensed production dataset and adapters, professionally reviewed multilanguage support, large independent real-world evaluations, production authentication, secure audit trail, public hosting and domain-expert acceptance. Details: [Acceptance criteria](../../docs/ACCEPTANCE.md).

[All ten projects](../INDEX.md) · [Main repository](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development)

# AI Road Safety and Accident Hotspot Intelligence

![Original project cover](assets/cover.svg)

> **Status:** Demonstration-grade source code using synthetic examples; no real operational deployment, authorized live feed, or independently verified field impact.

**Public need / intended users:** Finding geographic crash concentrations without claiming unadjusted counts measure actual personal risk. **Audience:** Road safety analysts and city planners.

**Technical evidence:** Spatial aggregation • explanatory analytics • GIS. Validated latitude/longitude and 0.01° grid aggregation over synthetic coordinates; no causal attribution or prediction.

## Reproducible setup

From the project branch root:

```bash
pip install -r requirements.txt
python cli.py
uvicorn app.main:app --reload
pytest -q
python cli.py
```

**API endpoint:** `POST /api/v1/analyze`

**Example payload:** [sample_request.json](sample_request.json). The FastAPI interactive schema is at `http://127.0.0.1:8000/docs`.

## Architecture, graphics and reproducibility

![Architecture illustration](assets/architecture.svg)

![Illustrative, fictional-data graphic](assets/synthetic-trend.svg)

- [Workflow source](docs/workflow.mmd) and [detailed architecture](docs/ARCHITECTURE.md).
- [Model card and evaluation plan](docs/MODEL_CARD.md), [threat model](docs/THREAT_MODEL.md).
- Synthetic fixture: `sample_request.json`; run in `cli.py`.
- Shared service: `app/` (model and routing implementation), `tests/` (automated checks), `Dockerfile`, and the local pytest suite.
- Frontend dashboard: `frontend/index.html`; this requires the API server to function.

## Dataset / source trust

**Planned authorized sources:** Licensed historical crash data, road network and traffic exposure (NOT connected). Demonstration data is fabricated; no source licensing or source freshness has been verified through a real ingest.

## Evaluation: do not fabricate results

**Measure:** Spatial holdout hit rate; exposure-adjusted hotspot precision once real data exists. The shared forecast modules report baseline and model MAE on chronological holdout when enough observations are provided. Running the evaluation script computes a small synthetic retrieval smoke test. Neither proves live field accuracy.

## Responsible AI constraints

No claims about an individual driver or causality from the fixture. Report uncertainty and require human approval for consequential decisions.

**Not yet complete:** licensed production dataset and adapters, professionally reviewed multilanguage support, large independent real-world evaluations, production authentication, secure audit trail, public hosting and domain-expert acceptance. Details: [Acceptance criteria](docs/ACCEPTANCE.md).

[Portfolio collection](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/main/public-benefit-ai/projects) · [Main repository](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development)

## Independent branch packaging

This is a separate **branch**, not an independent GitHub repository. It has its own isolated root tree containing source code, a dedicated API and web UI, tests, SVG diagrams and Docker Compose. No authorized live feeds or operational validation.

Start with `docker compose up --build`. Open `http://127.0.0.1:5173` or `http://127.0.0.1:8000/docs`.

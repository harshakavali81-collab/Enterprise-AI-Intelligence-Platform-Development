# AI Air Quality and Environmental Health Monitor

![Original project cover](assets/cover.svg)

> **Status:** Demonstration-grade source code using synthetic examples; no real operational deployment, authorized live feed, or independently verified field impact.

**Public need / intended users:** Studying local pollution trends while avoiding fabricated live readings or personal medical conclusions. **Audience:** Environment analysts studying pollutant time series.

**Technical evidence:** Air readings • lag forecasting • uncertainty limits. Lagged Ridge forecast for PM2.5 synthetic series; chronological holdout versus persistence, input quality checks.

## Reproducible setup

Start from this standalone branch root:

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
- Shared service: `app/` (model and routing implementation), `tests/` (automated checks), `Dockerfile`, and this repository's pytest suite.
- Frontend dashboard: `frontend/index.html`; this requires the API server to function.

## Dataset / source trust

**Planned authorized sources:** CPCB / data.gov.in licensed monitor data and weather (NOT connected). Demonstration data is fabricated; no source licensing or source freshness has been verified through a real ingest.

## Evaluation: do not fabricate results

**Measure:** MAE/RMSE per station and horizon, missing-sensor robustness, interval coverage. The shared forecast modules report baseline and model MAE on chronological holdout when enough observations are provided. Running the evaluation script computes a small synthetic retrieval smoke test. Neither proves live field accuracy.

## Responsible AI constraints

Missing measurements are not zero pollution; no personalized health advice. Report uncertainty and require human approval for consequential decisions.

**Not yet complete:** licensed production dataset and adapters, professionally reviewed multilanguage support, large independent real-world evaluations, production authentication, secure audit trail, public hosting and domain-expert acceptance. Details: [Acceptance criteria](docs/ACCEPTANCE.md).

[Collection](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/main/public-benefit-ai/projects) · [Main repository](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development)


## Source distribution

This project is published in a **standalone branch of the Enterprise AI repository**, not a newly created separate GitHub repository. Run `docker compose up --build` to start the API and browser on ports 8000 and 5173. Fixture is synthetic. Authorized real-world deployment has not been validated.

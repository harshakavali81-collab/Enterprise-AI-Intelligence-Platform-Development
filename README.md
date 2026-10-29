# AI Scam, Phishing and Digital Fraud Awareness Assistant

![Original project cover](assets/cover.svg)

> **Status:** Demonstration-grade source code using synthetic examples; no real operational deployment, authorized live feed, or independently verified field impact.

**Public need / intended users:** Helping users notice likely phishing signals while avoiding falsely declaring any message safe. **Audience:** Everyday users reviewing suspicious messages.

**Technical evidence:** NLP classifier • URL indicators • safe inspection. TF-IDF logistic regression trained on tiny labeled synthetic texts; URL parsing without visiting the link.

## Reproducible setup

From the root of this standalone branch:

```bash
pip install -r requirements.txt
python cli.py
uvicorn app.main:app --reload
python -m pytest -q
python -m pytest -q
```

**API endpoint:** `POST /api/v1/analyze`

**Example payload:** [sample_request.json](sample_request.json). The FastAPI interactive schema is at `http://127.0.0.1:8000/docs`.

## Architecture, graphics and reproducibility

![Architecture illustration](assets/architecture.svg)

![Illustrative, fictional-data graphic](assets/synthetic-trend.svg)

- [Workflow source](docs/workflow.mmd) and [detailed architecture](docs/ARCHITECTURE.md).
- [Model card and evaluation plan](docs/MODEL_CARD.md), [threat model](docs/THREAT_MODEL.md).
- Synthetic fixture: `sample_request.json`; run in `cli.py`.
- Shared service: `app/` (model and routing implementation), `tests/` (automated checks), `Dockerfile`, and local pytest suite.
- Frontend dashboard: `frontend/index.html`; this requires the API server to function.

## Dataset / source trust

**Planned authorized sources:** Licensed phishing corpora and authorized threat feeds (NOT connected). Demonstration data is fabricated; no source licensing or source freshness has been verified through a real ingest.

## Evaluation: do not fabricate results

**Measure:** Classwise precision, recall, PR-AUC and false-positive rate on future non-synthetic holdouts. The shared forecast modules report baseline and model MAE on chronological holdout when enough observations are provided. Running the evaluation script computes a small synthetic retrieval smoke test. Neither proves live field accuracy.

## Responsible AI constraints

Never open suspicious links or claim a non-flagged message is definitely legitimate. Report uncertainty and require human approval for consequential decisions.

**Not yet complete:** licensed production dataset and adapters, professionally reviewed multilanguage support, large independent real-world evaluations, production authentication, secure audit trail, public hosting and domain-expert acceptance. Details: [Acceptance criteria](docs/ACCEPTANCE.md).

[Ten-project collection](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/main/public-benefit-ai/projects) · [Main repository](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development)


## Branch packaging status

This is a **standalone branch of the Enterprise AI repository**, not a separate GitHub repository. Its root contains a directly runnable app, a one-project UI, CI tests, Docker Compose, original images and documentation. Production validation and authorized official feeds are outstanding.

Run the browser UI at `http://127.0.0.1:5173` and the API at `http://127.0.0.1:8000/docs` using `docker compose up --build`.

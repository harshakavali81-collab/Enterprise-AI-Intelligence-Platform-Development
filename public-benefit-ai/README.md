# Public Benefit AI — Ten Evidence-First Engineering Demonstrations

> **Status: runnable local synthetic-data portfolio prototypes; NOT live safety systems.** No operational alert feeds, protected-person records, verified third-party model metrics, official approvals, or public deployment are claimed.

Ten project topics match the supplied blueprint exactly. Each uses a suitable method (retrieval, interpretable ML baselines, geospatial counting, text classification or privacy-conscious deduplication) rather than making every project a chatbot.

## Run

```bash
cd public-benefit-ai
python -m venv .venv
# activate virtual environment
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
pytest -q
python -m scripts.evaluate
```

Docker: `docker compose up --build` starts both the API at `http://127.0.0.1:8000/docs` and the static frontend at `http://127.0.0.1:5173`. Both host ports bind to localhost only; no public production hosting is performed.

- `GET /health` — operational status.
- `GET /api/v1/projects` — 10 project labels and methods.
- `POST /api/v1/{slug}/analyze` — engine-specific JSON request, eg `{"text":"How to prepare for a flood?"}`.
- Optional `observations` for two forecasting modules; `events` for road hotspot count; `candidate` and `existing` for private matching.

## Run the interactive local dashboard

```bash
# In a first terminal
uvicorn app.main:app --reload
# In a second terminal
python -m http.server 5173 --directory frontend
```

Open `http://127.0.0.1:5173`, select a project and run its synthetic input using the local API. The dashboard does not work from GitHub Pages without a running backend; the portfolio link shows case studies and graphics, not a hosted API.

## Create ten genuinely independent repositories

`python scripts/export_standalone.py --replace` creates ten standalone folders, each with project-specific source/docs/fixtures, a one-project local frontend, Docker configuration, tests and CI. `--publish` additionally requires **GitHub CLI signed into an account authorized to create repos**; it never overwrites an existing repository. For verified procedure see [REPOSITORY_PUBLISHING.md](docs/REPOSITORY_PUBLISHING.md). The connected GitHub integration cannot create repositories in this session; ten distinct remote repos remain **not created**.

## Evidence and engineering

- 10 domain-specific projects (folders in `projects/`) with local synthetic fixtures, evaluation objectives, safety cases, workflows, original SVG diagrams and graphics.
- Shared API with schema checks, small test suite, deterministic baselines and generated synthetic evaluation file.
- Automated CI, Docker, demo user interface, explicit provenance and limits.
- Evaluation numbers are **not fabricated**: calculate your own results by running `python -m scripts.evaluate`.
- User input is not persisted by this demo service. Do not use sensitive case data; the `role` value is not a substitute for authentication.
- URLs in documents are never automatically fetched. RAG demo source passages are **fictional**, not authorized government publications.

## Trust and release gate

Before an operational product: authorized source integrations and licensing, provenance review, real-world labeled data, tested multilingual models, independent field evaluation, professional oversight, hardened authentication/authorization, rate-limits, audit retention, threat assessment, privacy review, hosting and incident procedures. See `docs/ACCEPTANCE.md`.

## Project collection

See `projects/INDEX.md` for direct links to every project. This collection is within an **existing** repository rather than ten new independent repositories.

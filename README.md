# Enterprise AI Intelligence Platform

An enterprise-oriented AI application that combines document retrieval, analytics, machine-learning predictions, and approval-based workflows behind a FastAPI service and React interface. It is a portfolio/demo project: validate configuration, access controls, and model outputs before using it with real business data.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Project diagram / illustration](<portfolio/assets/mobilitypulse/01-hero.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

- Document ingestion, chunking, retrieval, reranking, and cited answers
- Read-only SQL analytics with query validation
- Customer churn, demand forecasting, and anomaly-detection endpoints
- Agent orchestration for knowledge, SQL, ML, and report requests
- Human approval workflows, JWT authentication, and role-aware permissions
- React dashboard, PostgreSQL with pgvector, Redis, and MLflow integrations

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<public-benefit-ai/docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development.git
cd Enterprise-AI-Intelligence-Platform-Development
```

Prerequisites: Python 3.11 or newer, Node.js 20, and Docker Desktop with Docker Compose v2.

1. Copy `.env.example` to `.env` and set a unique `SECRET_KEY`, database password, and any provider credentials you need. Do not use the example values in a deployed environment.
2. Install the Python dependencies and create the sample data and local SQLite database:

   ```sh
   python -m pip install -r requirements.txt
   python generate_data.py
   ```

3. Start the data services and API:

   ```sh
   docker compose up --build
   ```

4. Open the frontend at `http://localhost:3000`, API documentation at `http://localhost:8000/docs`, and health status at `http://localhost:8000/health`.

To run the backend without Docker, create and activate a virtual environment, install `requirements.txt`, start PostgreSQL with pgvector and Redis, then run:

```sh
uvicorn backend.main:app --reload
```

For frontend development, run `npm ci` and `npm start` from `frontend/`. Set `REACT_APP_API_URL` when the API is not available at the default local address.

## Challenges & Solutions

**Repository organization:** this project uses `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

An enterprise-oriented AI application that combines document retrieval, analytics, machine-learning predictions, and approval-based workflows behind a FastAPI service and React interface. It is a portfolio/demo project: validate configuration, access controls, and model outputs before using it with real business data.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `sql/` | SQL schema and analysis |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

See [LICENSE](LICENSE) for the existing terms.

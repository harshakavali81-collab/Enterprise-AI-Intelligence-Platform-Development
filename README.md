# Enterprise AI Intelligence Platform

An enterprise-oriented AI application that combines document retrieval, analytics, machine-learning predictions, and approval-based workflows behind a FastAPI service and React interface. It is a portfolio/demo project: validate configuration, access controls, and model outputs before using it with real business data.

## Capabilities

- Document ingestion, chunking, retrieval, reranking, and cited answers
- Read-only SQL analytics with query validation
- Customer churn, demand forecasting, and anomaly-detection endpoints
- Agent orchestration for knowledge, SQL, ML, and report requests
- Human approval workflows, JWT authentication, and role-aware permissions
- React dashboard, PostgreSQL with pgvector, Redis, and MLflow integrations

## Run locally

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

3. Open the frontend at `http://localhost:3000`, API documentation at `http://localhost:8000/docs`, and health status at `http://localhost:8000/health`.

To run the backend without Docker, create and activate a virtual environment, install `requirements.txt`, start PostgreSQL with pgvector and Redis, then run:

```sh
uvicorn backend.main:app --reload
```

For frontend development, run `npm ci` and `npm start` from `frontend/`. Set `REACT_APP_API_URL` when the API is not available at the default local address.

## Validate

```sh
python generate_data.py
python -m pytest tests/ -q
flake8 backend/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

Build the frontend with `npm ci` followed by `npm run build` from `frontend/`. The CI workflow also exercises backend tests, frontend build, and Docker image builds.

## Project map

- `backend/`: API routes, agents, RAG, ML, security, database, and services
- `frontend/`: React and TypeScript user interface
- `sql/`: database schema and analytics queries
- `data/sample/`: sample documents and tabular data
- `evaluation/` and `tests/`: evaluation datasets, scripts, and automated tests
- `docs/`: architecture, workflow, security, API, evaluation, and deployment notes
- `dashboard/`, `notebooks/`, `reports/`, `presentation/`: analytics and project deliverables

## Configuration and limitations

The API uses the configured database and external LLM/provider credentials where enabled. Set a strong secret and review CORS, exposed ports, sample data, and database permissions before deployment. External provider calls and production-grade infrastructure are not required for the automated unit tests. See [deployment notes](docs/11_Deployment.md) and [security notes](docs/09_Security.md) for additional context.

## License

See [LICENSE](LICENSE).
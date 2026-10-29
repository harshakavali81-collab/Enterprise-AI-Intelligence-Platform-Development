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

4. Open the frontend at `http://localhost:3000`, API documentation at `http://localhost:8000/docs`, and health status at `http://localhost:8000/health`.

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

## 10 new AI/ML engineering demonstrations (October 2026)

**[Browse the ten-project collection](ten-ml-projects-2026/README.md)** · **[Portfolio showcase](https://github.com/harshakavali81-collab/harshavardhan-portfolio/blob/main/ml-projects.html)**

1. [Real-Time Fraud Detection and Risk Scoring Platform](ten-ml-projects-2026/01-real-time-fraud-detection-and-risk-scoring-platform/README.md)
2. [Retail Demand Forecasting and Inventory Optimization](ten-ml-projects-2026/02-retail-demand-forecasting-and-inventory-optimization/README.md)
3. [Customer Churn Prediction and Retention Intelligence](ten-ml-projects-2026/03-customer-churn-prediction-and-retention-intelligence/README.md)
4. [Computer Vision Quality Inspection System](ten-ml-projects-2026/04-computer-vision-quality-inspection-system/README.md)
5. [Personalized Recommendation Engine](ten-ml-projects-2026/05-personalized-recommendation-engine/README.md)
6. [Multilingual Semantic Search and Knowledge Assistant](ten-ml-projects-2026/06-multilingual-semantic-search-and-knowledge-assistant/README.md)
7. [Predictive Maintenance and Anomaly Detection](ten-ml-projects-2026/07-predictive-maintenance-and-anomaly-detection/README.md)
8. [Credit Risk and Loan Default Prediction](ten-ml-projects-2026/08-credit-risk-and-loan-default-prediction/README.md)
9. [Medical Image Classification Research Assistant](ten-ml-projects-2026/09-medical-image-classification-research-assistant/README.md)
10. [End-to-End MLOps Model Deployment Platform](ten-ml-projects-2026/10-end-to-end-mlops-model-deployment-platform/README.md)

Each folder contains source, unit tests, FastAPI, Docker, model/data documentation, architecture SVG, model metrics JSON and evaluation SVG based on **synthetic or bundled sample data**. All ten local smoke-test suites passed before publication; remote GitHub Actions status must be checked independently. None of these projects claims validated banking/medical/industrial decisions, real integrations, or public production hosting. New standalone repositories were not created because the available GitHub integration cannot create repositories.

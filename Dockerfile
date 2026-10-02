# ========================================================
# ENTERPRISE AI PLATFORM - PRODUCTION DOCKERFILE
# Multi-stage build for Backend & Frontend
# ========================================================

FROM python:3.11-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt constraints-docker.txt .
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple \
    --constraint constraints-docker.txt \
    -r requirements.txt

COPY backend/ /app/backend/
COPY sql/ /app/sql/
COPY data/ /app/data/
COPY generate_data.py /app/generate_data.py

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ── Guild AI Backend ──
FROM python:3.11-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services /app/services
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# Environment
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Create non-root user
RUN useradd --create-home guild
USER guild

EXPOSE 8000

# Default: run the API server
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

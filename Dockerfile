# ── Guild AI Production Build ──
# Multi-stage: Node build frontend → Python serve backend + static

# Stage 1: Build frontend
FROM node:22-alpine AS frontend-builder
WORKDIR /app/web
COPY services/web/package*.json ./
RUN npm ci --production=false
COPY services/web/ ./
RUN npm run build

# Stage 2: Production backend
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY services/ services/
COPY alembic/ alembic/
COPY alembic.ini .

# Copy frontend build from Stage 1
COPY --from=frontend-builder /app/web/dist services/web/dist

# Environment
ENV PYTHONUNBUFFERED=1
ENV PORT=8001

# Non-root user
RUN useradd --create-home guild
USER guild

EXPOSE 8001

# Default: run the API server (serves frontend via StaticFiles mount)
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8001"]

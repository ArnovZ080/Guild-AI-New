# Build Stage for Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/services/web
COPY services/web/package*.json ./
RUN npm install
COPY services/web/ ./
RUN npm run build

# Final Stage for Backend + Frontend Production
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY services /app/services
COPY main.py /app/main.py 2>/dev/null || true

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/services/web/dist /app/services/web/dist

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Command to run (assuming a main entrypoint that mounts the frontend)
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8080"]

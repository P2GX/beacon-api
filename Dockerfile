# Multi-stage Dockerfile for Beacon API

# Stage 1: Builder
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml README.md ./

# Create virtual environment and install dependencies
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache .

# Stage 2: Runtime
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 beacon && \
    mkdir -p /app && \
    chown -R beacon:beacon /app

# Copy virtual environment from builder
COPY --from=builder --chown=beacon:beacon /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=beacon:beacon src/ ./src/

# Switch to non-root user
USER beacon

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/monitor/health')"

# Run the application
CMD ["uvicorn", "beacon_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

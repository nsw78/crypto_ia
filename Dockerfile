FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Python deps - install both API and original requirements
COPY requirements-api.txt requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements-api.txt && \
    pip install streamlit && \
    pip install -r requirements.txt 2>/dev/null || true

# Application code
COPY . .

# Create data directory for SQLite and set permissions
RUN mkdir -p /app/data

# Non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000 8501

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# -------------------------------------------------------
# 1. Base image
# -------------------------------------------------------
FROM python:3.11-slim AS base

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# -------------------------------------------------------
# 2. Install system dependencies
# -------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------
# 3. Set working directory
# -------------------------------------------------------
WORKDIR /app

# -------------------------------------------------------
# 4. Copy project files
# -------------------------------------------------------
COPY requirements.txt .

# -------------------------------------------------------
# 5. Install Python dependencies
# -------------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code
COPY src ./src
COPY logs ./logs
COPY README.md .
COPY pyproject.toml .
COPY setup.cfg .

# Expose FastAPI port
EXPOSE 8000

# -------------------------------------------------------
# 6. Environment variables
# -------------------------------------------------------
ENV SENTINEL_LOG_DIR=/app/logs
ENV SENTINEL_RULES_FILE=/app/src/sentinellog/rules/rules.yaml
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# -------------------------------------------------------
# 7. Start command
# -------------------------------------------------------
# This launches FastAPI using uvicorn in production mode
CMD ["uvicorn", "src.sentinellog.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
# For development, you might want to use:
# CMD ["uvicorn", "src.sentinellog.api.main:app", "--host
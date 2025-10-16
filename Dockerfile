# ---- Base image ----
FROM python:3.12-slim

# ---- Working directory ----
WORKDIR /app

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy and install Python dependencies ----
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Copy source code ----
COPY . .

# ---- Expose port ----
EXPOSE 5000

# ---- Wait for PostgreSQL to be ready, then migrate and start ----
CMD ["bash", "-c", "until nc -z db 5432; do echo ' Waiting for PostgreSQL...'; sleep 2; done; echo 'DB ready!'; flask db upgrade && gunicorn -b 0.0.0.0:5000 'app:app'"]
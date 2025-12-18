FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (optional)
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy app
COPY . /app

# Render/Heroku-style runtime sets $PORT; ensure we bind to it
ENV PORT=8000

EXPOSE 8000

# Run migrations and optional seed, then start Gunicorn
# Set RUN_DB_MIGRATIONS=true and RUN_DB_SEED=true in Render to enable
CMD ["bash", "-lc", "\
if [ \"$RUN_DB_MIGRATIONS\" = \"true\" ]; then \
    echo 'Running Alembic migrations...'; \
    alembic upgrade head || exit 1; \
else \
    echo 'Skipping Alembic migrations'; \
fi; \
if [ \"$RUN_DB_SEED\" = \"true\" ]; then \
    echo 'Running seed script...'; \
    PYTHONPATH=. python scripts/seed_db.py || true; \
else \
    echo 'Skipping seed script'; \
fi; \
exec gunicorn app_server:app -b 0.0.0.0:${PORT} --workers 2"]

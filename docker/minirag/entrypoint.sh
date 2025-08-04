#!/bin/bash
set -e

echo "Running database migrations..."
cd /app/models/db_schemes/minirag/
alembic upgrade head
cd /app

echo "Starting FastAPI server..."
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
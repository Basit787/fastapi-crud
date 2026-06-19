#!/bin/bash

set -e

cleanup() {
    echo ""
    echo "Stopping Docker services..."
    docker compose down
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Starting Docker services..."
docker compose up -d

echo "Waiting for PostgreSQL to become healthy..."

until [ "$(docker inspect -f '{{.State.Health.Status}}' postgres)" = "healthy" ]; do
    sleep 2
done

echo "PostgreSQL is healthy"

echo "Syncing dependencies..."
uv sync

echo "Starting FastAPI..."
uv run uvicorn app.main:app --reload --port 2000

# If uvicorn exits normally
cleanup
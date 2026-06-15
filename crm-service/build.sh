#!/usr/bin/env bash
# build.sh — Render build script for the CRM service.
#
# Render runs this during every deploy. It:
#   1. Installs Python deps
#   2. Builds the React frontend into frontend/dist/
#   3. Runs Alembic migrations against the live DB
#   4. Seeds the DB if empty (idempotent — skips if data exists)

set -o errexit  # exit on error

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Installing frontend dependencies..."
cd frontend
npm install
echo "==> Building frontend..."
npm run build
cd ..

echo "==> Running database migrations..."
alembic upgrade head

echo "==> Seeding database (skips if already seeded)..."
python seed.py

echo "==> Build complete!"

#!/usr/bin/env bash
# build.sh — Render build script for the channel service.

set -o errexit

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Build complete!"

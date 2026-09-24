#!/usr/bin/env bash

set -e

PUZZLE_TYPE=$1

if [ ! -d ".venv" ]; then
    echo "Setting up the application..."
    python3 -m venv .venv

    echo "Installing dependencies..."
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install .

    echo "Installing Chromium..."
    .venv/bin/python -m playwright install chromium
fi

echo "Starting application..."
.venv/bin/python run.py "$PUZZLE_TYPE"
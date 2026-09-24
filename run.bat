@echo off
setlocal

if not exist ".venv" (
    echo Setting up the application...
    python -m venv .venv

    echo Installing dependencies...
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install .

    echo Installing Chromium...
    .venv\Scripts\python.exe -m playwright install chromium
)

echo Starting application...
.venv\Scripts\python.exe run.py

pause

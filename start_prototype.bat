@echo off
title Forest Vision AI - Prototype Server
echo ========================================================
echo   Forest Vision AI (VanaRakshak) Prototype
echo   PCCOE International Grand Challenge 2026 (Indradhanu)
echo ========================================================
echo.
cd /d "%~dp0"

echo [1/2] Checking Python Virtual Environment...
if exist ".venv\Scripts\python.exe" (
    echo Virtual environment detected.
) else (
    echo Creating virtual environment...
    python -m venv .venv
    echo Installing dependencies...
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo.
echo [2/2] Launching Forest Vision AI Dashboard...
start "" http://127.0.0.1:8000
.\.venv\Scripts\python.exe app.py
pause

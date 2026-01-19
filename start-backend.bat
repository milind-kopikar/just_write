@echo off
set PORT=8000
echo Starting Just Write Backend...
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port %PORT%

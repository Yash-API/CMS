@echo off
REM Batch script to run the backend FastAPI app with correct working directory

REM Change directory to the backend folder
cd /d %~dp0

REM Run uvicorn with app.main:app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

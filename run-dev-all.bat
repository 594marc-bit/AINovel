@echo off
title AINovel Development Servers

echo ========================================
echo Starting AINovel Development Environment
echo ========================================
echo.

REM Check if Python virtual environment exists
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

echo.
echo [1/2] Starting Backend Server (port 8000)...
cd backend
call venv\Scripts\activate
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..

echo.
echo [2/2] Starting Frontend Server (port 9000)...
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

if not exist ".env.local" (
    echo Creating .env.local file...
    echo API_BASE_URL=http://localhost:8000/api > .env.local
)

start "Frontend Server" cmd /k "npm run dev"

echo.
echo ========================================
echo Servers are starting...
echo.
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:9000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit...
pause > nul
@echo off
echo ========================================
echo Restarting Frontend Development Server
echo ========================================
echo.

REM Kill any existing Node.js processes on port 9000
echo Stopping any existing frontend server...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":9000" ^| find "LISTENING"') do (
    echo Killing process %%a...
    taskkill /f /pid %%a 2>nul
)

REM Wait a moment
timeout /t 2 /nobreak > nul

echo.
echo Starting frontend server...
echo The frontend will be available at: http://localhost:9000
echo.

REM Start the development server
npm run dev
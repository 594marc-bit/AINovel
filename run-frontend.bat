@echo off
echo Starting frontend development server...
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

REM Check if .env.local exists, if not create it
if not exist ".env.local" (
    echo Creating .env.local file...
    echo API_BASE_URL=http://localhost:8000/api > .env.local
)

echo.
echo Starting Quasar development server...
echo The frontend will be available at: http://localhost:9000
echo.
npm run dev
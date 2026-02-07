@echo off
echo.
echo ========================================
echo   Starting ClassAI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install dependencies if needed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo [OK] Dependencies installed
echo.

REM Start backend server
echo Starting backend server on port 8001...
start "ClassAI Backend" python main.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo Starting frontend server on port 3001...
echo.
echo ========================================
echo   ClassAI is running!
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:3001
echo.
echo API Documentation:
echo   http://localhost:8001/docs
echo.
echo Press Ctrl+C to stop the frontend server
echo (Backend will continue running in separate window)
echo ========================================
echo.

python -m http.server 3001

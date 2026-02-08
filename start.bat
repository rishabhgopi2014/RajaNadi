@echo off
REM Rajanadi Astro - Startup Script (Batch)
REM Launches both backend and frontend services

echo ==================================
echo   Rajanadi Astrology App Startup
echo ==================================
echo.

echo [1/4] Checking Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    [OK] Ollama is running
) else (
    echo    [WARNING] Ollama is not running!
    echo    Please start Ollama first: ollama serve
    echo    Press any key to continue anyway...
    pause >nul
)

echo.
echo [2/4] Starting Backend API...
start "Rajanadi Backend" cmd /k "cd /d %~dp0backend && if exist venv (call venv\Scripts\activate.bat && echo [VENV] Activated) else (echo [WARN] venv not found - using system Python) && echo Backend API Server && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
echo    [OK] Backend starting on http://127.0.0.1:8000
timeout /t 3 /nobreak >nul

echo.
echo [3/4] Starting Frontend...
start "Rajanadi Frontend" cmd /k "cd /d %~dp0frontend && echo Frontend Dev Server && npm run dev"
echo    [OK] Frontend starting on http://localhost:5173

echo.
echo [4/4] Services Started!
echo.
echo ==========================================
echo  Access Points:
echo    Frontend:  http://localhost:5173
echo    Backend:   http://127.0.0.1:8000
echo    API Docs:  http://127.0.0.1:8000/docs
echo ==========================================
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo Press any key to exit this window...
echo (Backend and Frontend will continue running)
pause >nul

@echo off
setlocal
echo ========================================
echo   Rajanadi Astrology - First Time Setup
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Check for Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo [1/3] Setting up Python Environment (Backend)...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b 1
)

echo.
echo [2/3] Setting up Node Environment (Frontend)...
cd ..\frontend

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Node dependencies.
        pause
        exit /b 1
    )
) else (
    echo Node dependencies already installed. Skipping npm install.
    echo (Delete 'node_modules' folder to force reinstall)
)

cd ..

echo.
echo [3/3] Setup Complete!
echo ========================================
echo.
echo You can now start the application by running:
echo    start.bat
echo.
echo NOTE: Make sure Ollama is running with 'ollama serve'
echo.
pause

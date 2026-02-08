@echo off
echo Stopping Rajanadi Astrology App...
echo.

echo [1/2] Stopping Backend (Python)...
taskkill /F /IM python.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Backend stopped
) else (
    echo    [INFO] Backend was not running or could not be stopped
)

echo.
echo [2/2] Stopping Frontend (Node)...
taskkill /F /IM node.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Frontend stopped
) else (
    echo    [INFO] Frontend was not running or could not be stopped
)

echo.
echo ==========================================
echo    All services stopped successfully!
echo ==========================================
pause

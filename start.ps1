# Rajanadi Astro - Startup Script (PowerShell)
# Launches both backend and frontend services

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Rajanadi Astrology App Startup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is running
Write-Host "[1/4] Checking Ollama..." -ForegroundColor Yellow
$ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if ($null -eq $ollamaProcess) {
    Write-Host "   ⚠️  Ollama is not running!" -ForegroundColor Red
    Write-Host "   Please start Ollama first: ollama serve" -ForegroundColor Red
    Write-Host "   Or press any key to continue anyway..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} else {
    Write-Host "   ✅ Ollama is running" -ForegroundColor Green
}

# Start Backend
Write-Host ""
Write-Host "[2/4] Starting Backend API..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'Backend API Server' -ForegroundColor Cyan; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

Write-Host "   ✅ Backend starting on http://127.0.0.1:8000" -ForegroundColor Green
Start-Sleep -Seconds 3

# Start Frontend
Write-Host ""
Write-Host "[3/4] Starting Frontend..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Frontend Dev Server' -ForegroundColor Cyan; npm run dev"

Write-Host "   ✅ Frontend starting on http://localhost:5173" -ForegroundColor Green

# Display URLs
Write-Host ""
Write-Host "[4/4] Services Started!" -ForegroundColor Green
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📡 Access Points:" -ForegroundColor White
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "   Backend:   http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "   API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop services" -ForegroundColor Yellow
Write-Host ""

# Open browser
Start-Sleep -Seconds 5
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

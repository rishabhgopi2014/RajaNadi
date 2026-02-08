# Setup Guide

Complete installation and setup instructions for RajanadiAstro.

## Prerequisites

### Required Software
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Ollama** - [Install Guide](https://ollama.ai/)

### Optional Tools
- **Git** - For cloning the repository
- **VS Code** - Recommended IDE

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd RajanadiAstro
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Ollama Setup

```bash
# Install Ollama (if not already installed)
# Follow instructions at https://ollama.ai/

# Pull the llama3 model
ollama pull llama3
```

## Configuration

### Backend Configuration

No configuration needed! The backend uses default settings:
- **Host**: 127.0.0.1
- **Port**: 8000
- **Ayanamsa**: Lahiri (auto-calculated)

### Frontend Configuration

Frontend automatically connects to:
- **API URL**: http://127.0.0.1:8000

## Running the Application

### Option 1: Use Startup Script (Recommended)

```bash
# From project root
.\start.bat
```

This will:
1. Start the backend server
2. Start the frontend dev server
3. Open your browser automatically

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access the Application:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Verification

### Check Backend Health

```bash
curl http://127.0.0.1:8000/api/health
```

Expected response:
```json
{"status": "healthy", "ollama_status": "running"}
```

### Test Chart Calculation

1. Open http://localhost:3000
2. Enter birth details
3. Click "Calculate Chart"
4. Verify charts display correctly

## Troubleshooting

### Backend Won't Start

**Problem**: Port 8000 already in use
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Problem**: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Start

**Problem**: Port 3000 already in use
```bash
# The script will offer to use a different port
# Or kill the existing process
```

** Problem**: Dependencies error
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Ollama Not Working

**Problem**: Connection refused
```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull llama3
```

**Problem**: Slow predictions
- This is normal for first-time model loading
- Subsequent predictions will be faster
- Consider using a smaller model if needed

### Charts Not Displaying

**Problem**: Blank charts
- Check browser console for errors
- Verify backend is running
- Ensure birth details are valid

**Problem**: Wrong ascendant position
- This is a known limitation without Swiss Ephemeris
- See [Ascendant Calculation](advanced/calculations.md#ascendant) for details

## Next Steps

- Read the [Quick Start Guide](quickstart.md)
- Explore [Features](features/chart-calculation.md)
- Learn about [Raja Nadi Rules](advanced/rajanadi-rules.md)

## Advanced Setup

### Installing Swiss Ephemeris (Optional)

For more accurate ascendant calculations:

```bash
# Install Visual C++ Build Tools first
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

pip install pyswisseph
```

See [PYSWISSEPH_INSTALL.md](../backend/PYSWISSEPH_INSTALL.md) for details.

### Custom Ayanamsa

To use a different ayanamsa, modify `backend/app/services/chart_calculator.py`:

```python
# Line ~175
ayanamsa = 23.85 + ((year - 2000) * 0.01397)  # Lahiri
# or
ayanamsa = 24.14  # Raman
```

### Port Configuration

Change backend port in `backend/app/main.py` and update frontend API URL in `frontend/src/components/BirthDetailsForm.jsx`.

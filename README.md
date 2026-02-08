# Rajanadi Astrology Application

A comprehensive Vedic astrology application using Rajanadi Shastra principles, powered by AI.

## 🚀 Quick Start

### Option 1: First Time Setup (One-Click)
Double-click `setup.bat` to automatically:
1. Create a Python virtual environment
2. Install all backend dependencies
3. Install all frontend dependencies

### Option 2: Automated Startup
**Windows Batch:**
```cmd
start.bat
```
This will:
1. Check/Activate the virtual environment
2. Check if Ollama is running
3. Start the backend API server (port 8000)
4. Start the frontend dev server (port 5173)
5. Open your browser automatically

### Option 2: Manual Startup

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

**Terminal 3 - Ollama:**
```bash
ollama serve
```

## 📦 Prerequisites

Before first run, ensure you have:

1. **Python 3.9+** installed
2. **Node.js 18+** and npm installed
3. **Ollama** installed and llama3 model pulled:
   ```bash
   ollama pull llama3
   ollama serve
   ```

4. **Backend dependencies** installed:
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install astropy skyfield  # Alternative to pyswisseph
   ```

5. **Frontend dependencies** installed:
   ```bash
   cd frontend
   npm install
   ```

## 🌐 Access Points

Once started, access the application at:

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs (Swagger UI)
- **Health Check**: http://127.0.0.1:8000/api/health

## 📁 Project Structure

```
RajanadiAstro/
├── backend/             # Python FastAPI backend
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── services/        # Chart calculator, Rajanadi engine, AI
│   │   ├── models/          # Pydantic data models
│   │   └── api/             # REST endpoints
│   ├── knowledge_base/
│   │   └── RajaNadiRules.txt  # 199KB Rajanadi rules
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   └── package.json
├── start.ps1            # PowerShell startup script
├── start.bat            # Batch startup script
└── README.md
```

## ✨ Features

- **Accurate Vedic Charts**: Natal (D1) and Navamsa (D9) using Skyfield ephemeris
- **Rajanadi System**: Authority Planet, 100% Conjunction Rule, Orb Analysis
- **AI Predictions**: Powered by Ollama llama3 model
- **Transit Analysis**: Current and future 24-month predictions
- **Pattern Matching**: Fast keyword-based rule retrieval

## 🛠️ Technology Stack

### Backend
- FastAPI (Python web framework)
- Skyfield (planetary calculations)
- Ollama (AI predictions)
- Pydantic (data validation)

### Frontend
- React 18
- Vite (build tool)
- Axios (API client)
- React Hook Form (forms)

## 📖 Usage

1. Run the startup script (`start.ps1` or `start.bat`)
2. Wait for both services to start
3. Browser will open automatically to http://localhost:5173
4. Enter birth details (Name, Date, Time, Place)
5. Click "Generate Prediction"
6. View comprehensive Rajanadi analysis

## 🐛 Troubleshooting

### Ollama Not Running
```bash
ollama serve
ollama pull llama3
```

### Port Already in Use
- Backend (8000): Check if another uvicorn instance is running
- Frontend (5173): Check if another Vite server is running

### Dependencies Not Installed
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## 📝 Notes

- **Skyfield vs Swiss Ephemeris**: We use Skyfield instead of pyswisseph due to compilation issues on newer Python versions/Windows
- **First Run**: Skyfield will download ~17MB ephemeris data (de421.bsp) automatically
- **Ollama Required**: Make sure Ollama is running before generating predictions

## 📚 Documentation

- See `backend/README.md` for backend API details
- See `MASTER_PROMPT_Rajanadi_Astro.md` for complete technical specs
- See `walkthrough.md` for implementation details

## 🎯 Quick Test

Test the API directly:
```bash
curl -X POST http://127.0.0.1:8000/api/generate-prediction \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "date_of_birth": "1990-01-01",
    "time_of_birth": "10:30:00",
    "place_of_birth": "Mumbai, India"
  }'
```

## 📄 License

Educational/Personal Use

---

**Enjoy exploring Rajanadi Astrology! 🌟**

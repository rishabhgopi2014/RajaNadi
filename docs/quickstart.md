# Quick Start Guide

Get RajanadiAstro running in 5 minutes!

## Prerequisites Check

✅ Python 3.9+ installed?  
✅ Node.js 16+ installed?  
✅ Ollama installed?

If not, see [Setup Guide](setup.md).

## 5-Minute Setup

### Step 1: Clone & Navigate (30 seconds)

```bash
cd C:\Users\Admin\OneDrive\Documents\RajanadiAstro
```

### Step 2: Install Dependencies (2 minutes)

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Step 3: Start Application (1 minute)

```bash
# From project root
cd ..
.\start.bat
```

The script will:
- Start backend on http://127.0.0.1:8000
- Start frontend on http://localhost:3000
- Open your browser automatically

### Step 4: Calculate Your First Chart (30 seconds)

1. **Enter your birth details**:
   - Name
   - Date of birth
   - Time of birth  
   - Place (city, state, country)
   - Coordinates (auto-filled from suggestions)

2. **Click "Calculate Chart"**

3. **View your charts**:
   - Natal Chart (D1) - South Indian format
   - Navamsa Chart (D9)
   - Authority Planet
   - Lucky Gemstone
   - Monthly Transits

### Step 5: Get AI Predictions (1 minute)

1. Click "**View AI Predictions**"
2. Wait ~10 seconds for AI to generate
3. Read personalized Raja Nadi predictions!

## That's It! 🎉

You now have a fully functional Vedic astrology application powered by AI.

## Next Steps

- **Learn Features**: [Chart Calculation](features/chart-calculation.md)
- **Understand Transits**: [Transit Analysis](features/transits.md)
- **Deep Dive**: [Architecture](architecture.md)
- **Raja Nadi**: [Advanced Rules](advanced/rajanadi-rules.md)

## Troubleshooting

**Backend won't start?**
```bash
# Check if port 8000 is free
netstat -ano | findstr :8000
```

**Frontend won't start?**
```bash
# Check if port 3000 is free
# The script will offer alternative ports
```

**Ollama not responding?**
```bash
# Start Ollama service
ollama serve

# Pull llama3 model
ollama pull llama3
```

**Still having issues?** See [Full Setup Guide](setup.md)

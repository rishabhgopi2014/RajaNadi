# Rajanadi Astrology Application - Backend

A comprehensive Vedic astrology prediction system using Rajanadi Shastra principles, Swiss Ephemeris for calculations, and Ollama LLM for AI-powered predictions.

## Features

- **Accurate Chart Calculations**: Uses Swiss Ephemeris with Lahiri ayanamsa
- **Rajanadi System**: Implements Authority Planet, 100% Conjunction Rule, Orb Rule
- **AI Predictions**: Ollama LLM generates personalized predictions
- **Pattern Matching**: Fast keyword-based rule retrieval (no vector embeddings!)
- **Transit Predictions**: Calculate future planetary transits for next 24 months

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Install Ollama

Download and install Ollama from https://ollama.ai

```bash
ollama pull llama3
ollama serve  # Runs on http://localhost:11434
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- **Swagger Docs**: http://localhost:8000/docs
- **API Base**: http://localhost:8000/api

## API Endpoints

### POST `/api/calculate-chart`
Calculate natal and navamsa charts

**Request Body:**
```json
{
  "name": "Ramanathan",
  "date_of_birth": "1990-05-15",
  "time_of_birth": "14:30:00",
  "place_of_birth": "Chennai, India"
}
```

### POST `/api/generate-prediction`
Generate complete astrological prediction

**Request Body:** Same as calculate-chart

**Response:** Includes natal chart, navamsa, authority planet, AI prediction text, current transits, and future triggers

### GET `/api/transits/current`
Get current planetary positions

### GET `/api/health`
Health check endpoint

## Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── models/                    # Pydantic models
│   ├── services/                  # Core services
│   │   ├── chart_calculator.py    # Swiss Ephemeris calculations
│   │   ├── rajanadi_engine.py     # Rajanadi rules implementation
│   │   ├── rules_matcher.py       # Pattern matching for rules
│   │   ├── ollama_service.py      # AI prediction generation
│   │   ├── timezone_service.py    # Geocoding & timezones
│   │   └── ephemeris_service.py   # Transit calculations
│   └── api/
│       └── routes.py              # API endpoints
├── knowledge_base/
│   └── RajaNadiRules.txt          # 199KB Rajanadi rules
└── requirements.txt
```

## Testing

Test with curl:
```bash
curl -X POST http://localhost:8000/api/generate-prediction \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "date_of_birth": "1990-01-01",
    "time_of_birth": "10:30:00",
    "place_of_birth": "Mumbai, India"
  }'
```

## Technologies

- **FastAPI**: Modern Python web framework
- **Swiss Ephemeris**: Accurate planetary calculations
- **Ollama + llama3**: Local LLM for predictions
- **geopy**: Geocoding for location → coordinates
- **pytz**: Timezone handling

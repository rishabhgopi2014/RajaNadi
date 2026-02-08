# Architecture Overview

RajanadiAstro follows a modern three-tier architecture with a React frontend, FastAPI backend, and Ollama AI service.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                   (React Frontend)                          │
│  - Birth Details Form                                       │
│  - South Indian Charts (D1, D9)                            │
│  - Transit Displays                                         │
│  - AI Predictions                                           │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/REST API
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER                            │
│                    (FastAPI + Python)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ API Layer (routes.py)                               │    │
│  │  - /api/calculate-chart                            │    │
│  │  - /api/predict                                     │    │
│  │  - /api/health                                      │    │
│  └───┬─────────────────────────────────────────────────┘    │
│      │                                                       │
│  ┌───▼───────────────────────────────────────────────┐     │
│  │ Service Layer                                     │     │
│  │  - chart_calculator.py (Natal/Navamsa)           │     │
│  │  - ephemeris_service.py (Transits)               │     │
│  │  - rajanadi_engine.py (Authority Planet)         │     │
│  │  - ollama_service.py (AI Integration)            │     │
│  │  - gemstone_service.py (Recommendations)         │     │
│  │  - monthly_transit_service.py                    │     │
│  │  - comprehensive_transit_service.py              │     │
│  └───┬───────────────────────────────────────────────┘     │
│      │                                                       │
│  ┌───▼───────────────────────────────────────────────┐     │
│  │ Core Libraries                                    │     │
│  │  - Skyfield (Astronomical Calculations)          │     │
│  │  - datetime (Date/Time Handling)                 │     │
│  │  - Pydantic (Data Validation)                    │     │
│  └───────────────────────────────────────────────────┘     │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP API
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI SERVICE                                │
│                    (Ollama + llama3)                        │
│  - Text Generation                                          │
│  - Raja Nadi Rule Application                              │
│  - Personalized Predictions                                 │
└─────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend (React)

**Location**: `frontend/src/`

#### Component Structure
```
frontend/src/
├── components/
│   ├── BirthDetailsForm.jsx    # User input form
│   ├── ChartsPage.jsx          # Chart visualization page
│   ├── SouthIndianChart.jsx    # South Indian chart renderer
│   └── PredictionsPage.jsx     # AI predictions display
├── App.jsx                      # Main app component & routing
└── App.css                      # Styling
```

#### Key Technologies
- **React 18** - UI framework
- **React Router** - Page navigation
- **Vite** - Build tool
- **Modern CSS** - Glassmorphism, gradients, animations

### Backend (FastAPI)

**Location**: `backend/app/`

#### Directory Structure
```
backend/app/
├── api/
│   └── routes.py               # API endpoints
├── models/
│   ├── chart_data.py          # Data models
│   └── prediction.py          # Response models
├── services/
│   ├── chart_calculator.py    # Core calculations
│   ├── ephemeris_service.py   # Transit calculations
│   ├── rajanadi_engine.py     # Raja Nadi logic
│   ├── ollama_service.py      # AI integration
│   ├── gemstone_service.py    # Gemstone recommendations
│   ├── monthly_transit_service.py
│   └── comprehensive_transit_service.py
└── main.py                     # FastAPI app initialization
```

#### Key Technologies
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Skyfield** - Astronomical calculations
- **Uvicorn** - ASGI server

### AI Service (Ollama)

**Local Installation**

- **Model**: llama3 (8B parameters)
- **Purpose**: Generate personalized predictions
- **Integration**: REST API via `ollama_service.py`

## Data Flow

### Chart Calculation Flow

```
1. User enters birth details
   ↓
2. Frontend sends POST /api/calculate-chart
   ↓
3. chart_calculator.py:
   - Calculates Julian Day
   - Gets planetary positions from Skyfield
   - Applies Lahiri Ayanamsa
   - Determines rasis (signs)
   - Detects retrograde planets
   ↓
4. rajanadi_engine.py:
   - Identifies Authority Planet
     Priority: Retrograde → Edge → Exalted
   ↓
5. ephemeris_service.py:
   - Calculates future transits
   - Groups conjunctions
   ↓
6. gemstone_service.py:
   - Recommends gemstone for Authority Planet
   ↓
7. Frontend displays:
   - South Indian Charts
   - Planetary positions
   - Authority planet
   - Monthly transits
   - Sign changes & retrogrades
```

### Prediction Flow

```
1. User requests prediction
   ↓
2. Frontend sends POST /api/predict
   ↓
3. ollama_service.py:
   - Loads Raja Nadi rules from knowledge_base/
   - Constructs prompt with:
     * Natal chart positions
     * Current transits
     * Authority planet
     * Retrograde planets
     * Raja Nadi rules
   ↓
4. Ollama API:
   - Processes with llama3 model
   - Generates personalized prediction
   ↓
5. Frontend displays formatted prediction
```

## Key Design Decisions

### 1. Sidereal vs Tropical

**Choice**: Sidereal (Vedic) system with Lahiri Ayanamsa

**Rationale**: Raja Nadi astrology is based on Vedic principles which use the sidereal zodiac.

### 2. South Indian Chart Format

**Choice**: Rectangular South Indian format

**Rationale**: 
- Traditional and authentic
- Clear visual representation
- Familiar to Vedic astrology practitioners

### 3. Local AI (Ollama)

**Choice**: Local Ollama instead of cloud API

**Rationale**:
- Privacy - birth data never leaves local machine
- Cost - no API fees
- Speed - low latency
- Offline capability

### 4. Retrograde Priority

**Choice**: Retrograde planets given highest priority for Authority Planet

**Rationale**: Raja Nadi principle that retrograde planets have amplified influence.

### 5. Latitude Correction

**Choice**: Simple `latitude * 0.5` correction for ascendant

**Rationale**: Balance between accuracy and complexity without requiring Swiss Ephemeris C++ compilation.

## Security Considerations

### Data Privacy
- **No external API calls** for calculations
- **No data storage** - all calculations are real-time
- **No user accounts** - no authentication needed

### CORS Configuration
- **Restricted to localhost** - `allow_origins=["http://localhost:3000"]`
- **Safe for local use** - not currently production-hardened

## Performance Characteristics

### Chart Calculation
- **Latency**: < 100ms
- **Complexity**: O(n) where n = number of planets

### Transit Calculation
- **Latency**: ~500ms for 12 months
- **Sampling**: Daily for sign change detection

### AI Predictions
- **First Request**: 10-30 seconds (model loading)
- **Subsequent**: 3-10 seconds
- **Depends on**: Hardware, model size, prompt length

## Scalability

### Current Limitations
- **Single-user focus** - designed for local desktop use
- **No caching** - calculations performed fresh each time
- **No database** - stateless architecture

### Future Enhancements
- Multi-user support with authentication
- Result caching (Redis)
- Database for chart storage (PostgreSQL)
- Async task queue for predictions (Celery)

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 + Vite | UI and visualization |
| Backend | FastAPI + Python 3.9 | RESTful API |
| Calculations | Skyfield | Astronomical ephemeris |
| AI | Ollama + llama3 | Predictions |
| Server | Uvicorn | ASGI web server |
| Validation | Pydantic | Data models |

## Next Steps

- [Setup Guide](setup.md) - Install and configure
- [API Reference](api/README.md) - Endpoint documentation
- [Service Documentation](backend/services.md) - Service layer details

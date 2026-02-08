# API Reference

Complete reference for all RajanadiAstro backend API endpoints.

## Base URL

```
http://127.0.0.1:8000
```

## Interactive Documentation

FastAPI provides auto-generated interactive docs:
- **Swagger UI**: http://127.0.0.1: 8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Endpoints

### POST /api/calculate-chart

Calculate natal and navamsa charts with transits.

#### Request

**Content-Type**: `application/json`

```json
{
  "name": "John Doe",
  "date_of_birth": "1983-08-08",
  "time_of_birth": "04:30:00",
  "place_of_birth": "Chennai, Tamil Nadu, India",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "timezone": "Asia/Kolkata"
}
```

#### Response

**Status**: `200 OK`

```json
{
  "natal": {
    "Sun": {
      "longitude": 111.234,
      "rasi": 4,
      "rasi_name": "Cancer",
      "degree": 21.23,
      "is_retrograde": false,
      "speed": 0.957
    },
    ...
  },
  "navamsa": { ... },
  "authority_planet": "Jupiter",
  "future_transits": [...],
  "monthly_transits": [...],
  "sign_changes": {...},
  "retrograde_periods": [...],
  "lucky_gemstone": {
    "gemstone": "Yellow Sapphire",
    "planet": "Jupiter",
    "benefits": "...",
    "day": "Thursday",
    "finger": "Index finger"
  }
}
```

---

### POST /api/predict

Generate AI-powered predictions based on natal chart and transits.

#### Request

```json
{
  "name": "John Doe",
  "natal_chart": { ... },
  "authority_planet": "Jupiter",
  "current_transits": { ... }
}
```

#### Response

```json
{
  "name": "John Doe",
  "natal_chart": { ... },
  "navamsa_chart": { ... },
  "authority_planet": "Jupiter",
  "prediction_text": "Based on your chart...",
  "current_transits": { ... },
  "future_triggers": [...],
  "matched_rules_count": 15
}
```

---

### GET /api/health

Check API and Ollama service health.

#### Response

```json
{
  "status": "healthy",
  "ollama_status": "running"
}
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid date format"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Chart calculation error: ..."
}
```

## Rate Limiting

Currently **no rate limiting** - designed for local single-user use.

## Authentication

Currently **no authentication required** - local deployment only.

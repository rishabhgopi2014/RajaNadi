"""
FastAPI main application
Rajanadi Astrology Prediction System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-Powered Rajanadi Vedic Astrology Predictions using Ollama LLM"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Rajanadi Astrology API",
        "version": settings.VERSION,
        "endpoints": {
            "calculate_chart": f"{settings.API_PREFIX}/calculate-chart",
            "generate_prediction": f"{settings.API_PREFIX}/generate-prediction",
            "current_transits": f"{settings.API_PREFIX}/transits/current",
            "health": f"{settings.API_PREFIX}/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

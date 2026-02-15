from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime

from app.models.birth_details import BirthDetails

from app.schemas import PredictionRequest, PredictionResponse, ChartResponse
from app.services.chart_calculator import ChartCalculator
from app.services.rajanadi_engine import RajanadiEngine
from app.services.ephemeris_service import EphemerisService
from app.services.ollama_service import OllamaService
from app.services.gemstone_service import gemstone_service
from app.services.monthly_transit_service import MonthlyTransitService

from app.services.comprehensive_transit_service import ComprehensiveTransitService
from app.services.rules_matcher import rules_matcher

router = APIRouter()

# Initialize services
chart_calculator = ChartCalculator()
rajanadi_engine = RajanadiEngine()
ephemeris_service = EphemerisService()
ollama_service = OllamaService()
monthly_transit_service = MonthlyTransitService()
comprehensive_transit_service = ComprehensiveTransitService()

@router.post("/calculate-chart", response_model=ChartResponse)
async def calculate_chart(birth_details: BirthDetails):
    """Calculate natal and navamsa charts with transit information"""
    try:
        # Parse birth details
        # Parse birth details
        year = birth_details.date_of_birth.year
        month = birth_details.date_of_birth.month
        day = birth_details.date_of_birth.day
        
        hour = birth_details.time_of_birth.hour
        minute = birth_details.time_of_birth.minute
        second = birth_details.time_of_birth.second
        
        # Calculate natal chart
        natal = chart_calculator.calculate_natal_chart(
            year, month, day, hour, minute, second,
            birth_details.latitude, birth_details.longitude
        )
        
        # Calculate navamsa (D9) chart
        navamsa = chart_calculator.calculate_navamsa(natal)
        
        # Identify authority planet using Raja Nadi rules
        authority = rajanadi_engine.identify_authority_planet(natal)
        
        # Calculate future transits
        future_transits = ephemeris_service.get_future_transits(natal, months_ahead=12)
        
        # Calculate monthly transits
        monthly_transits = monthly_transit_service.get_monthly_transits(months_ahead=6)
        
        # Get comprehensive transit data (sign changes and retrograde periods)
        current_year = datetime.now().year
        sign_changes = comprehensive_transit_service.get_sign_changes(year=current_year)
        retrograde_periods = comprehensive_transit_service.get_retrograde_periods(year=current_year)
        
        # Get gemstone recommendation for authority planet
        gemstone_data = gemstone_service.get_gemstone_recommendation(authority)
        
        # Format gemstone info properly for frontend
        lucky_gemstone = {
            "gemstone": gemstone_data.get('primary', 'Consult astrologer'),
            "planet": authority,
            "benefits": gemstone_data.get('benefits', ''),
            "finger": gemstone_data.get('finger', 'As per astrologer'),
            "day": gemstone_data.get('day', 'Auspicious day'),
            "mantra": gemstone_data.get('mantra', '')
        }
        
        return ChartResponse(
            natal=natal,
            navamsa=navamsa,
            authority_planet=authority,
            future_transits=future_transits[:20],  # Top 20 upcoming transits
            monthly_transits=monthly_transits,  # Monthly planetary positions
            sign_changes=sign_changes,  # Major planet sign changes
            retrograde_periods=retrograde_periods,  # Retrograde periods table
            lucky_gemstone=lucky_gemstone  # Use formatted dict
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart calculation error: {str(e)}")

@router.post("/generate-prediction", response_model=PredictionResponse)
async def get_prediction(request: PredictionRequest):
    """Generate AI-powered predictions using Raja Nadi principles"""
    try:
        # Prepare birth data
        birth_data = {
            "name": request.name,
            "date_of_birth": request.date_of_birth if request.date_of_birth else "Unknown",
            "time_of_birth": request.time_of_birth if request.time_of_birth else "Unknown",
            "place_of_birth": request.place_of_birth if request.place_of_birth else "Unknown"
        }

        
        # Prepare chart analysis
        # Extract natal planets from the request dict
        natal_planets = request.natal_chart.get('planets', request.natal_chart)
        navamsa_chart = request.navamsa_chart if hasattr(request, 'navamsa_chart') else {}
        
        # Get full analysis
        chart_analysis = rajanadi_engine.analyze_chart(natal_planets, navamsa_chart)
        
        # Get matched rules
        matched_rules = rules_matcher.build_context_for_chart(chart_analysis)
        
        # Get prediction from Ollama service (Synchronous call)
        prediction_text = ollama_service.generate_prediction(
            birth_data=birth_data,
            chart_analysis=chart_analysis,
            transit_data={'current_positions': request.current_transits},
            matched_rules=matched_rules,
            category=request.category,
            custom_question=request.custom_question
        )
        
        return PredictionResponse(
            name=request.name,
            natal_chart=request.natal_chart,
            navamsa_chart=navamsa_chart,
            authority_planet=request.authority_planet,
            prediction_text=prediction_text,
            current_transits=request.current_transits if hasattr(request, 'current_transits') else {},
            future_triggers=[],
            matched_rules_count=len(matched_rules.split('\n\n---\n\n')) if matched_rules else 0
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/health")
async def health_check():
    """Check API health and Ollama service status"""
    ollama_status = await ollama_service.check_health()
    return {
        "status": "healthy",
        "ollama_status": "running" if ollama_status else "not available"
    }

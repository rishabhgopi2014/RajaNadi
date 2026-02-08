"""
Data models for chart information and prediction
(Consolidated form app.models.chart_data and app.models.prediction)
"""
from pydantic import BaseModel
from typing import Dict, List, Optional, Any


class PlanetPosition(BaseModel):
    """Position of a planet in the chart"""
    name: str
    longitude: float  # Absolute longitude (0-360)
    rasi: int  # Sign number (1-12)
    degree: float  # Degree within sign (0-30)
    is_retrograde: bool
    
class NatalChart(BaseModel):
    """Natal chart (D1/Rasi) data"""
    planets: Dict[str, PlanetPosition]
    ascendant: PlanetPosition
    
class NavamsaChart(BaseModel):
    """Navamsa chart (D9) data"""
    planets: Dict[str, Dict[str, Any]]  # planet -> {rasi, degree}
    
class ChartAnalysis(BaseModel):
    """Complete chart analysis for Rajanadi predictions"""
    authority_planet: Optional[str]
    retrogrades: List[str]
    exchanges: List[str]  # Parivartana yogas
    edge_planets: List[str]  # Planets at 0-2° or 28-30°
    conjunctions: List[Dict[str, Any]]
    karakas: Dict[str, Dict[str, Any]]  # Sun->Father, Moon->Mother, etc.
    
class TransitData(BaseModel):
    """Current and future transit information"""
    current_positions: Dict[str, PlanetPosition]
    future_triggers: List[Dict[str, Any]]  # Date, planet, impact

class PredictionResponse(BaseModel):
    """Complete prediction response"""
    name: str
    natal_chart: Dict
    navamsa_chart: Dict
    authority_planet: Optional[str]
    prediction_text: str
    current_transits: Dict
    future_triggers: List[Dict]
    matched_rules_count: int

class PredictionRequest(BaseModel):
    """Request for prediction generation"""
    name: str
    natal_chart: Dict
    navamsa_chart: Optional[Dict] = {}
    authority_planet: Optional[str]
    current_transits: Optional[Dict] = {}
    category: Optional[str] = "general"
    custom_question: Optional[str] = None

class ChartResponse(BaseModel):
    """Response for chart calculation only"""
    natal: Dict
    navamsa: Dict
    authority_planet: Optional[str]
    future_transits: List[Dict] = []  # Future planetary transits for the year
    monthly_transits: List[Dict] = []  # Monthly planetary positions
    sign_changes: Dict = {}  # Major planet sign changes 
    retrograde_periods: List[Dict] = []  # Retrograde periods
    lucky_gemstone: Optional[Dict] = None  # Gemstone recommendation based on authority planet

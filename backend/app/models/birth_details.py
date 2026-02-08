"""
Pydantic models for birth details input
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime, date, time
from typing import Optional

class BirthDetails(BaseModel):
    """Birth details for chart calculation"""
    name: str = Field(..., description="Person's full name")
    date_of_birth: date = Field(..., description="Date of birth (YYYY-MM-DD)")
    time_of_birth: time = Field(..., description="Time of birth (HH:MM:SS)")
    place_of_birth: str = Field(..., description="Place of birth (City, Country)")
    
    # Optional coordinates (will be geocoded if not provided)
    latitude: Optional[float] = Field(None, description="Latitude in decimal degrees")
    longitude: Optional[float] = Field(None, description="Longitude in decimal degrees")
    timezone: Optional[str] = Field(None, description="Timezone (e.g., 'Asia/Kolkata')")
    
    # Prediction options
    category: Optional[str] = Field("general", description="Prediction category: marriage, career, health, parents, children, wealth, custom, or general")
    custom_question: Optional[str] = Field(None, description="Custom question for personalized prediction")
    
    @validator('time_of_birth', pre=True)
    def parse_time(cls, v):
        if isinstance(v, str):
            # Handle various time formats: "HH:MM", "HH:MM:SS"
            if ':' in v:
                parts = v.split(':')
                hour = int(parts[0])
                minute = int(parts[1])
                second = int(parts[2]) if len(parts) > 2 else 0
                return time(hour, minute, second)
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ramanathan",
                "date_of_birth": "1990-05-15",
                "time_of_birth": "14:30:00",
                "place_of_birth": "Chennai, India"
            }
        }

class BirthDateTime(BaseModel):
    """Combined datetime model for calculations"""
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    latitude: float
    longitude: float
    timezone_offset: float  # Hours from UTC

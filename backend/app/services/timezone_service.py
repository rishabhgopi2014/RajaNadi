"""
Timezone and geocoding service
"""
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
from typing import Tuple, Optional

class TimezoneService:
    """Handle timezone conversions and geocoding"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="rajanadi_astro")
    
    def geocode_location(self, place_name: str) -> Tuple[float, float, str]:
        """
        Convert place name to coordinates and timezone
        
        Args:
            place_name: City, Country (e.g., "Chennai, India")
            
        Returns:
            (latitude, longitude, timezone_name)
        """
        try:
            location = self.geolocator.geocode(place_name)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                
                # Estimate timezone (simple mapping for Indian locations)
                # For production, use timezonefinder library
                if 'India' in place_name or 'Chennai' in place_name:
                    timezone_name = 'Asia/Kolkata'
                else:
                    timezone_name = 'UTC'  # Default
                
                return latitude, longitude, timezone_name
            else:
                # Default to Chennai if geocoding fails
                return 13.0827, 80.2707, 'Asia/Kolkata'
        
        except Exception as e:
            print(f"Geocoding error: {e}")
            # Default to Chennai
            return 13.0827, 80.2707, 'Asia/Kolkata'
    
    def get_utc_offset(self, timezone_name: str, date_time: datetime) -> float:
        """
        Get UTC offset for a timezone at a specific datetime
        
        Args:
            timezone_name: Timezone name (e.g., 'Asia/Kolkata')
            date_time: Datetime to check
            
        Returns:
            UTC offset in hours
        """
        try:
            tz = pytz.timezone(timezone_name)
            offset = tz.utcoffset(date_time)
            return offset.total_seconds() / 3600
        except:
            return 5.5  # Default to IST

# Global instance
timezone_service = TimezoneService()

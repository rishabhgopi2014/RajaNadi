from typing import Dict, List
from datetime import datetime, timedelta
from skyfield.api import load

class MonthlyTransitService:
    """Calculate monthly planetary positions and influences"""
    
    PLANET_INFLUENCES = {
        'Sun': 'Authority, vitality, career, father',
        'Moon': 'Mind, emotions, mother, public image',
        'Mars': 'Energy, courage, conflicts, property',
        'Mercury': 'Communication, intellect, business',
        'Jupiter': 'Wisdom, expansion, fortune, children',
        'Venus': 'Love, luxury, relationships, arts',
        'Saturn': 'Discipline, delays, karma, longevity',
        'Rahu': 'Obsession, worldly desires, sudden gains',
        'Ketu': 'Spirituality, detachment, past karma'
    }
    
    RASI_NAMES = [
        '', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self):
        self.ts = load.timescale()
        self.planets = load('de421.bsp')
        self.earth = self.planets['earth']
    
    def get_monthly_transits(self, months_ahead: int = 12) -> List[Dict]:
        """Get planetary positions for next N months"""
        monthly_data = []
        current_date = datetime.now()
        
        # Lahiri Ayanamsa for current year
        ayanamsa = 23.85 + ((current_date.year - 2000) * 0.01397)
        
        for month_offset in range(months_ahead):
            target_date = current_date + timedelta(days=30 * month_offset)
            t = self.ts.utc(target_date.year, target_date.month, target_date.day)
            
            month_transits = {
                'month': target_date.strftime('%B %Y'),
                'planets': []
            }
            
            # Calculate position for each planet
            planet_bodies = {
                'Sun': self.planets['sun'],
                'Moon': self.planets['moon'],
                'Mars': self.planets['mars'],
                'Mercury': self.planets['mercury'],
                'Jupiter': self.planets['jupiter barycenter'],
                'Venus': self.planets['venus'],
                'Saturn': self.planets['saturn barycenter']
            }
            
            for planet_name, planet_body in planet_bodies.items():
                try:
                    # Get tropical longitude
                    astrometric = self.earth.at(t).observe(planet_body)
                    lon, lat, distance = astrometric.ecliptic_latlon()
                    tropical_lon = lon.degrees
                    
                    # Convert to sidereal
                    sidereal_lon = (tropical_lon - ayanamsa) % 360
                    rasi = int(sidereal_lon / 30) + 1
                    
                    month_transits['planets'].append({
                        'name': planet_name,
                        'rasi': self.RASI_NAMES[rasi],
                        'influence': self.PLANET_INFLUENCES[planet_name]
                    })
                except:
                    continue
            
            monthly_data.append(month_transits)
        
        return monthly_data

# Global instance
monthly_transit_service = MonthlyTransitService()

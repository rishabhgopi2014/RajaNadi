from typing import Dict, List
from datetime import datetime, timedelta
from skyfield.api import load

class ComprehensiveTransitService:
    """Calculate comprehensive transits including sign changes and retrogrades"""
    
    RASI_NAMES = [
        '', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self):
        self.ts = load.timescale()
        self.planets = load('de421.bsp')
        self.earth = self.planets['earth']
    
    def get_sign_changes(self, year: int = 2026) -> Dict[str, List[Dict]]:
        """Calculate sign changes for major planets in the given year"""
        
        # Ayanamsa for the year
        ayanamsa = 23.85 + ((year - 2000) * 0.01397)
        
        sign_changes = {
            'Jupiter': [],
            'Saturn': [],
            'Rahu_Ketu': [],
            'Uranus': [],
            'Neptune': []
        }
        
        # Sample daily to detect sign changes
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        
        planet_bodies = {
            'Jupiter': self.planets['jupiter barycenter'],
            'Saturn': self.planets['saturn barycenter'],
            'Uranus': self.planets['uranus barycenter'],
            'Neptune': self.planets['neptune barycenter']
        }
        
        prev_signs = {}
        
        current = start_date
        while current <= end_date:
            t = self.ts.utc(current.year, current.month, current.day)
            
            for planet_name, planet_body in planet_bodies.items():
                try:
                    astrometric = self.earth.at(t).observe(planet_body)
                    lon, _, _ = astrometric.ecliptic_latlon()
                    tropical_lon = lon.degrees
                    sidereal_lon = (tropical_lon - ayanamsa) % 360
                    rasi = int(sidereal_lon / 30) + 1
                    
                    if planet_name not in prev_signs:
                        prev_signs[planet_name] = rasi
                    elif prev_signs[planet_name] != rasi:
                        sign_changes[planet_name].append({
                            'date': current.strftime('%B %d, %Y'),
                            'from_sign': self.RASI_NAMES[prev_signs[planet_name]],
                            'to_sign': self.RASI_NAMES[rasi]
                        })
                        prev_signs[planet_name] = rasi
                except:
                    continue
            
            current += timedelta(days=1)
        
        return sign_changes
    
    def get_retrograde_periods(self, year: int = 2026) -> List[Dict]:
        """Get retrograde periods for planets"""
        # Sample retrograde data for 2026 (would need ephemeris for exact calculation)
        retrogrades = [
            {
                'planet': 'Mercury',
                'periods': [
                    {'start': 'Feb 26', 'end': 'Mar 20', 'signs': 'Pisces'},
                    {'start': 'Jun 29', 'end': 'Jul 24', 'signs': 'Cancer/Gemini'},
                    {'start': 'Oct 24', 'end': 'Nov 13', 'signs': 'Scorpio/Libra'}
                ]
            },
            {
                'planet': 'Venus',
                'periods': [
                    {'start': 'Oct 3', 'end': 'Nov 14', 'signs': 'Scorpio/Libra'}
                ]
            },
            {
                'planet': 'Jupiter',
                'periods': [
                    {'start': '(From 2025)', 'end': 'Mar 11', 'signs': 'Cancer'},
                    {'start': 'Dec 13', 'end': '(Into 2027)', 'signs': 'Leo'}
                ]
            },
            {
                'planet': 'Saturn',
                'periods': [
                    {'start': 'Jul 27', 'end': 'Dec 11', 'signs': 'Pisces/Aries'}
                ]
            }
        ]
        
        return retrogrades

# Global instance
comprehensive_transit_service = ComprehensiveTransitService()

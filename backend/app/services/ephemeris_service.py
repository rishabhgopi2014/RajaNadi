"""
Ephemeris service for current and future transits using Skyfield
"""
from skyfield.api import load
from datetime import datetime, timedelta
from typing import Dict, List

class EphemerisService:
    """Calculate current and future planetary transits"""
    
    # Lahiri Ayanamsa
    LAHIRI_AYANAMSA_2000 = 23.85
    AYANAMSA_RATE = 0.01397
    
    def __init__(self):
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.earth = self.eph['earth']
        
        self.rasi_names = {
            1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
            5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
            9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"
        }
    
    def get_ayanamsa(self, year: float) -> float:
        """Calculate Lahiri ayanamsa"""
        years_from_2000 = year - 2000.0
        return self.LAHIRI_AYANAMSA_2000 + (years_from_2000 * self.AYANAMSA_RATE)
    
    def get_current_transits(self) -> Dict:
        """
        Get current planetary positions
        
        Returns:
            Dictionary with current planet positions
        """
        now = datetime.utcnow()
        t = self.ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)
        
        # Calculate ayanamsa
        decimal_year = now.year + (now.month - 1) / 12.0
        ayanamsa = self.get_ayanamsa(decimal_year)
        
        planets = {}
        
        planet_bodies = {
            'Sun': self.eph['sun'],
            'Moon': self.eph['moon'],
            'Mars': self.eph['mars'],
            'Mercury': self.eph['mercury'],
            'Jupiter': self.eph['jupiter barycenter'],
            'Venus': self.eph['venus'],
            'Saturn': self.eph['saturn barycenter']
        }
        
        for name, body in planet_bodies.items():
            try:
                pos = self.earth.at(t).observe(body)
                lon_tropical = pos.apparent().ecliptic_latlon()[1].degrees
                lon_sidereal = (lon_tropical - ayanamsa) % 360
                rasi = int(lon_sidereal / 30) + 1
                degree = lon_sidereal % 30
                
                planets[name] = {
                    'rasi': rasi,
                    'rasi_name': self.rasi_names[rasi],
                    'degree': round(degree, 2),
                    'longitude': round(lon_sidereal, 4)
                }
            except:
                # Default values if calculation fails
                planets[name] = {
                    'rasi': 1,
                    'rasi_name': 'Aries',
                    'degree': 0.0,
                    'longitude': 0.0
                }
        
        # Calculate Rahu (approximate)
        days_from_epoch = (t.tt - 2451545.0)
        rahu_lon_tropical = (125.0 - (days_from_epoch * 0.05295)) % 360
        rahu_lon_sidereal = (rahu_lon_tropical - ayanamsa) % 360
        rahu_rasi = int(rahu_lon_sidereal / 30) + 1
        
        planets['Rahu'] = {
            'rasi': rahu_rasi,
            'rasi_name': self.rasi_names[rahu_rasi],
            'degree': round(rahu_lon_sidereal % 30, 2),
            'longitude': round(rahu_lon_sidereal, 4)
        }
        
        # Ketu
        ketu_long = (rahu_lon_sidereal + 180) % 360
        planets['Ketu'] = {
            'rasi': int(ketu_long / 30) + 1,
            'rasi_name': self.rasi_names[int(ketu_long / 30) + 1],
            'degree': round(ketu_long % 30, 2),
            'longitude': round(ketu_long, 4)
        }
        
        return planets
    
    def get_future_transits(self, natal_planets: Dict, months_ahead: int = 24) -> List[Dict]:
        """
        Calculate future transits that trigger natal positions
        Focus on slow-moving planets: Saturn, Jupiter, Rahu, Ketu
        
        Args:
            natal_planets: Natal chart planet positions
            months_ahead: How many months ahead to calculate
            
        Returns:
            List of significant transit events
        """
        triggers = []
        slow_planets = ['Saturn', 'Jupiter']
        
        # Check every 15 days for the next N months
        days_to_check = months_ahead * 30
        
        for day_offset in range(0, days_to_check, 15):
            future_date = datetime.utcnow() + timedelta(days=day_offset)
            t = self.ts.utc(future_date.year, future_date.month, future_date.day, 12, 0, 0)
            
            decimal_year = future_date.year + (future_date.month - 1) / 12.0
            ayanamsa = self.get_ayanamsa(decimal_year)
            
            planet_bodies = {
                'Saturn': self.eph['saturn barycenter'],
                'Jupiter': self.eph['jupiter barycenter']
            }
            
            for planet_name, planet_body in planet_bodies.items():
                try:
                    pos = self.earth.at(t).observe(planet_body)
                    lon_tropical = pos.apparent().ecliptic_latlon()[1].degrees
                    transit_lon = (lon_tropical - ayanamsa) % 360
                    transit_rasi = int(transit_lon / 30) + 1
                    transit_degree = transit_lon % 30
                    
                    # Check if transit planet conjuncts any natal planet (same rasi)
                    for natal_name, natal_data in natal_planets.items():
                        if natal_name in ['Ascendant']:
                            continue
                        
                        natal_rasi = natal_data['rasi']
                        
                        # Check for conjunction (same sign)
                        if transit_rasi == natal_rasi:
                            # Check degree proximity (within 5°)
                            natal_degree = natal_data['degree']
                            
                            if abs(transit_degree - natal_degree) <= 5:
                                triggers.append({
                                    'date': future_date.strftime('%Y-%m-%d'),
                                    'transit_planet': planet_name,
                                    'natal_planet': natal_name,
                                    'rasi': self.rasi_names[transit_rasi],
                                    'type': 'conjunction',
                                    'impact': f"{planet_name} conjunct natal {natal_name}"
                                })
                except:
                    continue
        
        
        # Remove duplicates and group consecutive transits
        # Group by (transit_planet, natal_planet, rasi)
        grouped_transits = {}
        for trigger in triggers:
            key = (trigger['transit_planet'], trigger['natal_planet'], trigger['rasi'])
            if key not in grouped_transits:
                grouped_transits[key] = {
                    'dates': [],
                    'data': trigger
                }
            grouped_transits[key]['dates'].append(trigger['date'])
        
        # Create unique transits with date ranges
        unique_triggers = []
        for key, group in grouped_transits.items():
            dates = sorted(group['dates'])
            # If multiple consecutive dates, show as range
            if len(dates) > 1:
                date_str = f"{dates[0]} to {dates[-1]}"
            else:
                date_str = dates[0]
            
            transit = group['data'].copy()
            transit['date'] = date_str
            transit['date_start'] = dates[0]  # For sorting
            unique_triggers.append(transit)
        
        # Sort by first date
        unique_triggers.sort(key=lambda x: x['date_start'])
        
        return unique_triggers[:20]  # Return top 20 events

# Global instance
ephemeris_service = EphemerisService()

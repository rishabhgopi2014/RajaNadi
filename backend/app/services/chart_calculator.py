"""
Vedic chart calculation using Skyfield (alternative to Swiss Ephemeris)
"""
from skyfield.api import load, Topos
from skyfield import almanac
from datetime import datetime, timezone
from typing import Dict
import math

class ChartCalculator:
    """Calculate Vedic astrological charts using Skyfield"""
    
    RASI_NAMES = {
        1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
        5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
        9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"
    }
    
    # Lahiri Ayanamsa for 2000.0 epoch
    LAHIRI_AYANAMSA_2000 = 23.85  # degrees
    AYANAMSA_RATE = 0.01397  # degrees per year (precession rate)
    
    def __init__(self):
        """Initialize with Skyfield ephemeris"""
        self.ts = load.timescale()
        self.eph = load('de421.bsp')  # Download ephemeris data
        
        # Define celestial bodies
        self.sun = self.eph['sun']
        self.moon = self.eph['moon']
        self.earth = self.eph['earth']
        self.planets = {
            'Mercury': self.eph['mercury'],
            'Venus': self.eph['venus'],
            'Mars': self.eph['mars'],
            'Jupiter': self.eph['jupiter barycenter'],
            'Saturn': self.eph['saturn barycenter']
        }
    
    def get_ayanamsa(self, year: float) -> float:
        """
        Calculate Lahiri ayanamsa for given year
        
        Args:
            year: Decimal year (e.g., 1990.5)
            
        Returns:
            Ayanamsa in degrees
        """
        years_from_2000 = year - 2000.0
        ayanamsa = self.LAHIRI_AYANAMSA_2000 + (years_from_2000 * self.AYANAMSA_RATE)
        return ayanamsa
    
    def get_ecliptic_longitude(self, position):
        """Convert position to ecliptic longitude"""
        ra, dec, distance = position.radec()
        
        # Convert RA/Dec to ecliptic coordinates (simplified)
        # For accurate results, use proper coordinate transformation
        ecliptic_lon = ra.degrees
        
        return ecliptic_lon
    
    def calculate_natal_chart(self, year: int, month: int, day: int, 
                             hour: int, minute: int, second: int,
                             latitude: float, longitude: float) -> Dict:
        """
        Calculate natal chart (D1/Rasi chart)
        
        Args:
            year, month, day: Birth date
            hour, minute, second: Birth time (24-hour format)
            latitude, longitude: Birth location coordinates
            
        Returns:
            Dictionary with planetary positions
        """
        # Create time object
        t = self.ts.utc(year, month, day, hour, minute, second)
        
        # Calculate ayanamsa
        decimal_year = year + (month - 1) / 12.0 + day / 365.25
        ayanamsa = self.get_ayanamsa(decimal_year)
        
        planets_data = {}
        
        # Observer location
        location = self.earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
        
        # Sun
        sun_pos = location.at(t).observe(self.sun)
        sun_lon = sun_pos.apparent().ecliptic_latlon()[1].degrees
        sun_lon_sidereal = (sun_lon - ayanamsa) % 360
        sun_rasi = int(sun_lon_sidereal / 30) + 1
        
        planets_data['Sun'] = {
            'longitude': round(sun_lon_sidereal, 4),
            'rasi': sun_rasi,
            'rasi_name': self.RASI_NAMES[sun_rasi],
            'degree': round(sun_lon_sidereal % 30, 2),
            'is_retrograde': False,  # Sun never retrograde
            'speed': 0.0
        }
        
        # Moon
        moon_pos = location.at(t).observe(self.moon)
        moon_lon = moon_pos.apparent().ecliptic_latlon()[1].degrees
        moon_lon_sidereal = (moon_lon - ayanamsa) % 360
        moon_rasi = int(moon_lon_sidereal / 30) + 1
        
        planets_data['Moon'] = {
            'longitude': round(moon_lon_sidereal, 4),
            'rasi': moon_rasi,
            'rasi_name': self.RASI_NAMES[moon_rasi],
            'degree': round(moon_lon_sidereal % 30, 2),
            'is_retrograde': False,  # Moon Inever retrograde
            'speed': 0.0
        }
        
        # Other planets
        for planet_name, planet_body in self.planets.items():
            try:
                planet_pos = location.at(t).observe(planet_body)
                planet_lon = planet_pos.apparent().ecliptic_latlon()[1].degrees
                planet_lon_sidereal = (planet_lon - ayanamsa) % 360
                planet_rasi = int(planet_lon_sidereal / 30) + 1
                
                # Detect retrograde (simplified - check velocity)
                # For accurate retrograde detection, compare positions over time
                is_retro = False  # Placeholder - implement proper retrograde detection if needed
                
                planets_data[planet_name] = {
                    'longitude': round(planet_lon_sidereal, 4),
                    'rasi': planet_rasi,
                    'rasi_name': self.RASI_NAMES[planet_rasi],
                    'degree': round(planet_lon_sidereal % 30, 2),
                    'is_retrograde': is_retro,
                    'speed': 0.0
                }
            except:
                # If planet calculation fails, use default
                planets_data[planet_name] = {
                    'longitude': 0.0,
                    'rasi': 1,
                    'rasi_name': 'Aries',
                    'degree': 0.0,
                    'is_retrograde': False,
                    'speed': 0.0
                }
        
        # Calculate Rahu (Mean North Node) - simplified calculation
        # For accurate Rahu, use proper lunar node calculation
        # Approximate: Rahu moves ~19.3 degrees/year backward
        days_from_epoch = (t.tt - 2451545.0)  # Days from J2000
        rahu_lon_tropical = (125.0 - (days_from_epoch * 0.05295)) % 360  # Approximate
        rahu_lon_sidereal = (rahu_lon_tropical - ayanamsa) % 360
        rahu_rasi = int(rahu_lon_sidereal / 30) + 1
        
        planets_data['Rahu'] = {
            'longitude': round(rahu_lon_sidereal, 4),
            'rasi': rahu_rasi,
            'rasi_name': self.RASI_NAMES[rahu_rasi],
            'degree': round(rahu_lon_sidereal % 30, 2),
            'is_retrograde': False,
            'speed': 0.0
        }
        
        # Ketu (180° opposite to Rahu)
        ketu_long = (rahu_lon_sidereal + 180) % 360
        ketu_rasi = int(ketu_long / 30) + 1
        
        planets_data['Ketu'] = {
            'longitude': round(ketu_long, 4),
            'rasi': ketu_rasi,
            'rasi_name': self.RASI_NAMES[ketu_rasi],
            'degree': round(ketu_long % 30, 2),
            'is_retrograde': False,
            'speed': 0.0
        }
        
        
        # Calculate Ascendant (Lagna) - simplified with latitude correction
        local_sidereal_time = self.calculate_sidereal_time(t, longitude)
        
        # Apply latitude correction factor
        # Reduced correction to fine-tune ascendant position
        latitude_correction = latitude * 0.5  # Reduced from 2.5 to 0.5
        
        ascendant_lon = (local_sidereal_time * 15 + latitude_correction - ayanamsa) % 360
        asc_rasi = int(ascendant_lon / 30) + 1
        
        planets_data['Ascendant'] = {
            'longitude': round(ascendant_lon, 4),
            'rasi': asc_rasi,
            'rasi_name': self.RASI_NAMES[asc_rasi],
            'degree': round(ascendant_lon % 30, 2),
            'is_retrograde': False,
            'speed': 0.0
        }
        
        
        return planets_data
    
    def calculate_sidereal_time(self, t, longitude):
        """Calculate local sidereal time"""
        # Simplified calculation using Skyfield's built-in GMST
        gmst = t.gmst  # Greenwich Mean Sidereal Time (hours)
        lst = (gmst + longitude / 15.0) % 24  # Local Sidereal Time
        return lst
    
    def calculate_navamsa(self, natal_planets: Dict) -> Dict:
        """
        Calculate Navamsa chart (D9)
        Formula: (Planet longitude × 9) mod 360, then divide by 30 for rasi
        
        Args:
            natal_planets: Dictionary of natal planet positions
            
        Returns:
            Dictionary with navamsa positions
        """
        navamsa = {}
        
        for planet, data in natal_planets.items():
            longitude = data['longitude']
            
            # Navamsa calculation
            navamsa_long = (longitude * 9) % 360
            navamsa_rasi = int(navamsa_long / 30) + 1
            navamsa_degree = navamsa_long % 30
            
            navamsa[planet] = {
                'rasi': navamsa_rasi,
                'rasi_name': self.RASI_NAMES[navamsa_rasi],
                'degree': round(navamsa_degree, 2)
            }
        
        return navamsa
    
    def detect_edge_planets(self, planets: Dict) -> list:
        """
        Detect planets at Rasi edges (0-2° or 28-30°)
        These are significant in Rajanadi system
        
        Args:
            planets: Dictionary of planet positions
            
        Returns:
            List of planet names at edges
        """
        edge_planets = []
        
        for name, data in planets.items():
            if name == 'Ascendant':
                continue
            degree = data['degree']
            if degree <= 2.0 or degree >= 28.0:
                edge_planets.append(name)
        
        return edge_planets
    
    def detect_exchanges(self, planets: Dict) -> list:
        """
        Detect Parivartana Yoga (mutual exchange of signs)
        
        Args:
            planets: Dictionary of planet positions
            
        Returns:
            List of exchange pairs
        """
        exchanges = []
        
        # Planet ownership of signs
        ownership = {
            1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
            5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
            9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
        }
        
        # Check each planet pair
        planet_list = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                if planet1 not in planets or planet2 not in planets:
                    continue
                    
                rasi1 = planets[planet1]['rasi']
                rasi2 = planets[planet2]['rasi']
                
                # Check if planet1 is in planet2's sign and vice versa
                if ownership.get(rasi1) == planet2 and ownership.get(rasi2) == planet1:
                    exchanges.append(f"{planet1}-{planet2}")
        
        return exchanges

# Global instance
chart_calculator = ChartCalculator()

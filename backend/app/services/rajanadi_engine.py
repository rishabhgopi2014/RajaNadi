"""
Rajanadi Shastra Rule Engine
Implements core Rajanadi logic: Authority Planet, Conjunctions, Orb Rule, Karakas
"""
from typing import Dict, List, Optional, Tuple

class RajanadiEngine:
    """Core Rajanadi astrology rule implementation"""
    
    def identify_authority_planet(self, planets: Dict) -> Optional[str]:
        """
        Identify the Authority Planet (Adhikara Graham) using Rajanadi priority:
        1. Retrograde planets
        2. Planets in Exchange (Parivartana)
        3. Planets at Rasi edges (0-2° or 28-30°)
        4. Planets in Own/Exalted/Debilitated signs
        
        Args:
            planets: Dictionary of planet positions from chart_calculator
            
        Returns:
            Name of the Authority Planet
        """
        # Priority 1: Retrograde planets
        retrogrades = [name for name, data in planets.items() 
                      if data.get('is_retrograde', False) and name not in ['Ascendant', 'Rahu', 'Ketu']]
        if retrogrades:
            return retrogrades[0]  # First retrograde planet
        
        # Priority 2: Check for exchanges (handled separately, but check if exists)
        # This would require exchange detection from chart_calculator
        
        # Priority 3: Edge planets (0-2° or 28-30°)
        for name, data in planets.items():
            if name in ['Ascendant', 'Rahu', 'Ketu']:
                continue
            degree = data.get('degree', 0)
            if degree <= 2.0 or degree >= 28.0:
                return name
        
        # Priority 4: Planets in own/exalted/debilitated signs
        exaltation = {
            'Sun': 1,  # Aries
            'Moon': 2,  # Taurus
            'Mars': 10,  # Capricorn
            'Mercury': 6,  # Virgo
            'Jupiter': 4,  # Cancer
            'Venus': 12,  # Pisces
            'Saturn': 7,  # Libra
        }
        
        own_signs = {
            'Sun': [5],  # Leo
            'Moon': [4],  # Cancer
            'Mars': [1, 8],  # Aries, Scorpio
            'Mercury': [3, 6],  # Gemini, Virgo
            'Jupiter': [9, 12],  # Sagittarius, Pisces
            'Venus': [2, 7],  # Taurus, Libra
            'Saturn': [10, 11],  # Capricorn, Aquarius
        }
        
        for name, rasi in [(n, d['rasi']) for n, d in planets.items() if n not in ['Ascendant', 'Rahu', 'Ketu']]:
            if rasi == exaltation.get(name) or rasi in own_signs.get(name, []):
                return name
        
        # Default: Return strongest planet (Sun)
        return 'Sun'
    
    def find_conjunctions(self, planets: Dict) -> List[Dict]:
        """
        Find 100% conjunctions (1st, 5th, 7th, 9th Rasis)
        and 50% connections (3rd, 11th Rasis)
        
        Args:
            planets: Dictionary of planet positions
            
        Returns:
            List of conjunction dictionaries
        """
        conjunctions = []
        planet_list = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                rasi1 = planets[planet1]['rasi']
                rasi2 = planets[planet2]['rasi']
                
                # Calculate distance (considering circular zodiac)
                distance = (rasi2 - rasi1) % 12
                
                # Check for 100% conjunction (1st, 5th, 7th, 9th)
                if distance in [0, 4, 6, 8]:
                    strength = 100
                    type_name = f"{distance+1}th house" if distance > 0 else "same sign"
                # Check for 50% connection (3rd, 11th)
                elif distance in [2, 10]:
                    strength = 50
                    type_name = f"{distance+1}th house"
                else:
                    continue
                
                conjunctions.append({
                    'planet1': planet1,
                    'planet2': planet2,
                    'strength': strength,
                    'type': type_name,
                    'distance': distance + 1
                })
        
        return conjunctions
    
    def apply_orb_rule(self, planet_name: str, planets: Dict) -> List[Tuple[str, float]]:
        """
        Apply the 15-degree Orb Rule
        Planet influences ±15° from its position
        
        Args:
            planet_name: Name of the planet to check
            planets: Dictionary of all planet positions
            
        Returns:
            List of (planet_name, orb_influence) tuples
        """
        if planet_name not in planets:
            return []
        
        planet_long = planets[planet_name]['longitude']
        influenced = []
        
        for other_name, other_data in planets.items():
            if other_name == planet_name or other_name == 'Ascendant':
                continue
            
            other_long = other_data['longitude']
            
            # Calculate angular distance (shortest path)
            diff = abs(planet_long - other_long)
            if diff > 180:
                diff = 360 - diff
            
            # Check if within 15° orb
            if diff <= 15:
                influence_strength = 1.0 - (diff / 15.0) # Stronger when closer
                influenced.append((other_name, round(influence_strength, 2)))
        
        return influenced
    
    def analyze_karakas(self, planets: Dict) -> Dict:
        """
        Analyze planetary Karakas (significations) according to Rajanadi
        
        Karakas:
        - Sun: Father, Son, Authority
        - Moon: Mother, Mind, House
        - Mercury: Education, Daughter, Maternal Uncle
        - Venus: Wife, Wealth, Luxury
        - Mars: Brother/Husband (for females), Land, Debt
        - Jupiter: The Self (Jiva), Children, Wisdom
        - Saturn: Profession, Karma, Labor
        
        Args:
            planets: Dictionary of planet positions
            
        Returns:
            Dictionary with karaka analysis
        """
        karakas = {
            'Sun': {
                'significations': ['Father', 'Son', 'Authority', 'Government'],
                'rasi': planets['Sun']['rasi'],
                'rasi_name': planets['Sun']['rasi_name'],
                'degree': planets['Sun']['degree'],
                'is_retrograde': planets['Sun']['is_retrograde']
            },
            'Moon': {
                'significations': ['Mother', 'Mind', 'House', 'Travel'],
                'rasi': planets['Moon']['rasi'],
                'rasi_name': planets['Moon']['rasi_name'],
                'degree': planets['Moon']['degree'],
                'is_retrograde': planets['Moon']['is_retrograde']
            },
            'Mercury': {
                'significations': ['Education', 'Daughter', 'Maternal Uncle', 'Communication'],
                'rasi': planets['Mercury']['rasi'],
                'rasi_name': planets['Mercury']['rasi_name'],
                'degree': planets['Mercury']['degree'],
                'is_retrograde': planets['Mercury']['is_retrograde']
            },
            'Venus': {
                'significations': ['Wife', 'Wealth', 'Luxury', 'Art'],
                'rasi': planets['Venus']['rasi'],
                'rasi_name': planets['Venus']['rasi_name'],
                'degree': planets['Venus']['degree'],
                'is_retrograde': planets['Venus']['is_retrograde']
            },
            'Mars': {
                'significations': ['Brother', 'Husband (for females)', 'Land', 'Debt'],
                'rasi': planets['Mars']['rasi'],
                'rasi_name': planets['Mars']['rasi_name'],
                'degree': planets['Mars']['degree'],
                'is_retrograde': planets['Mars']['is_retrograde']
            },
            'Jupiter': {
                'significations': ['Self (Jiva)', 'Children', 'Wisdom', 'Gold'],
                'rasi': planets['Jupiter']['rasi'],
                'rasi_name': planets['Jupiter']['rasi_name'],
                'degree': planets['Jupiter']['degree'],
                'is_retrograde': planets['Jupiter']['is_retrograde']
            },
            'Saturn': {
                'significations': ['Profession', 'Karma', 'Labor', 'Older Brother'],
                'rasi': planets['Saturn']['rasi'],
                'rasi_name': planets['Saturn']['rasi_name'],
                'degree': planets['Saturn']['degree'],
                'is_retrograde': planets['Saturn']['is_retrograde']
            }
        }
        
        return karakas
    
    def analyze_chart(self, natal_planets: Dict, navamsa: Dict) -> Dict:
        """
        Complete chart analysis for Rajanadi predictions
        
        Args:
            natal_planets: Natal chart planet positions
            navamsa: Navamsa chart positions
            
        Returns:
            Complete analysis dictionary
        """
        authority = self.identify_authority_planet(natal_planets)
        conjunctions = self.find_conjunctions(natal_planets)
        karakas = self.analyze_karakas(natal_planets)
        
        # Get retrogrades
        retrogrades = [name for name, data in natal_planets.items() 
                      if data.get('is_retrograde', False) and name not in ['Ascendant', 'Rahu', 'Ketu']]
        
        # Get edge planets
        edge_planets = [name for name, data in natal_planets.items()
                       if name not in ['Ascendant', 'Rahu', 'Ketu'] and 
                       (data['degree'] <= 2.0 or data['degree'] >= 28.0)]
        
        return {
            'authority_planet': authority,
            'retrogrades': retrogrades,
            'edge_planets': edge_planets,
            'conjunctions': conjunctions,
            'karakas': karakas,
            'planets': natal_planets,
            'navamsa': navamsa
        }

# Global instance
rajanadi_engine = RajanadiEngine()

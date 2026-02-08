"""
Gemstone recommendations based on Vedic Astrology
"""

class GemstoneService:
    """Provide gemstone recommendations for planets"""
    
    # Gemstone mappings for each planet
    GEMSTONE_MAP = {
        'Sun': {
            'primary': 'Ruby',
            'alternative': ['Red Garnet', 'Red Spinel'],
            'benefits': 'Enhances leadership, confidence, vitality, and authority',
            'metal': 'Gold',
            'finger': 'Ring finger',
            'day': 'Sunday',
            'weight': '3-6 carats'
        },
        'Moon': {
            'primary': 'Pearl',
            'alternative': ['Moonstone', 'White Coral'],
            'benefits': 'Improves emotional balance, mental peace, and intuition',
            'metal': 'Silver',
            'finger': 'Little finger',
            'day': 'Monday',
            'weight': '4-7 carats'
        },
        'Mars': {
            'primary': 'Red Coral',
            'alternative': ['Carnelian', 'Red Jasper'],
            'benefits': 'Increases courage, energy, physical strength, and determination',
            'metal': 'Copper or Gold',
            'finger': 'Ring finger',
            'day': 'Tuesday',
            'weight': '5-8 carats'
        },
        'Mercury': {
            'primary': 'Emerald',
            'alternative': ['Green Tourmaline', 'Peridot'],
            'benefits': 'Enhances intelligence, communication, business acumen, and learning',
            'metal': 'Gold',
            'finger': 'Little finger',
            'day': 'Wednesday',
            'weight': '3-6 carats'
        },
        'Jupiter': {
            'primary': 'Yellow Sapphire',
            'alternative': ['Yellow Topaz', 'Citrine'],
            'benefits': 'Brings wisdom, prosperity, spiritual growth, and good fortune',
            'metal': 'Gold',
            'finger': 'Index finger',
            'day': 'Thursday',
            'weight': '3-6 carats'
        },
        'Venus': {
            'primary': 'Diamond',
            'alternative': ['White Sapphire', 'Zircon'],
            'benefits': 'Attracts love, luxury, artistic talents, and marital happiness',
            'metal': 'Silver or Platinum',
            'finger': 'Middle finger or Little finger',
            'day': 'Friday',
            'weight': '1-2 carats'
        },
        'Saturn': {
            'primary': 'Blue Sapphire',
            'alternative': ['Amethyst', 'Lapis Lazuli'],
            'benefits': 'Provides discipline, focus, longevity, and removes obstacles',
            'metal': 'Silver or Iron',
            'finger': 'Middle finger',
            'day': 'Saturday',
            'weight': '4-7 carats',
            'caution': 'Wear only after consultation - can have strong effects'
        },
        'Rahu': {
            'primary': 'Hessonite (Gomed)',
            'alternative': ['Garnet', 'Spessartite'],
            'benefits': 'Removes confusion, enhances worldly success, and protects from enemies',
            'metal': 'Silver',
            'finger': 'Middle finger',
            'day': 'Saturday',
            'weight': '5-8 carats'
        },
        'Ketu': {
            'primary': "Cat's Eye (Lehsunia)",
            'alternative': ['Tiger Eye', 'Chrysoberyl'],
            'benefits': 'Provides spiritual insight, protects from hidden enemies, and promotes moksha',
            'metal': 'Silver',
            'finger': 'Middle finger',
            'day': 'Tuesday',
            'weight': '4-7 carats'
        }
    }
    
    def get_gemstone_recommendation(self, planet: str) -> dict:
        """
        Get gemstone recommendation for a planet
        
        Args:
            planet: Planet name (Sun, Moon, Mars, etc.)
            
        Returns:
            Dictionary with gemstone details
        """
        return self.GEMSTONE_MAP.get(planet, {
            'primary': 'Consult an astrologer',
            'alternative': [],
            'benefits': 'Get personalized gemstone recommendation',
            'metal': 'Gold or Silver',
            'finger': 'As per consultation',
            'day': 'Auspicious day',
            'weight': 'As per consultation'
        })

# Global instance
gemstone_service = GemstoneService()

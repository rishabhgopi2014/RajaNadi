"""
Test script for Rajanadi Astrology backend
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.chart_calculator import chart_calculator
from app.services.rajanadi_engine import rajanadi_engine
from app.services.rules_matcher import rules_matcher

def test_chart_calculation():
    """Test basic chart calculation"""
    print("\n=== Testing Chart Calculation ===")
    
    # Test data: January 1, 1990, 10:30 AM, Chennai
    natal = chart_calculator.calculate_natal_chart(
        year=1990,
        month=1,
        day=1,
        hour=10,
        minute=30,
        second=0,
        latitude=13.0827,
   longitude=80.2707
    )
    
    print("\nNatal Chart:")
    for planet, data in natal.items():
        retro = " (R)" if data['is_retrograde'] else ""
        print(f"  {planet:12} - {data['rasi_name']:12} {data['degree']:5.2f}°{retro}")
    
    # Calculate Navamsa
    navamsa = chart_calculator.calculate_navamsa(natal)
    print("\nNavamsa Chart:")
    for planet, data in navamsa.items():
        print(f"  {planet:12} - {data['rasi_name']:12} {data['degree']:5.2f}°")
    
    return natal, navamsa

def test_rajanadi_engine(natal, navamsa):
    """Test Rajanadi engine"""
    print("\n=== Testing Rajanadi Engine ===")
    
    # Analyze chart
    analysis = rajanadi_engine.analyze_chart(natal, navamsa)
    
    print(f"\nAuthority Planet: {analysis['authority_planet']}")
    print(f"Retrogrades: {', '.join(analysis['retrogrades']) or 'None'}")
    print(f"Edge Planets: {', '.join(analysis['edge_planets']) or 'None'}")
    
    print(f"\nConjunctions ({len(analysis['conjunctions'])}):")
    for conj in analysis['conjunctions'][:5]:  # Show first 5
        print(f"  {conj['planet1']} <-> {conj['planet2']}: {conj['strength']}% ({conj['type']})")
    
    return analysis

def test_rules_matcher(analysis):
    """Test pattern matching"""
    print("\n=== Testing Rules Matcher ===")
    
    matched = rules_matcher.build_context_for_chart(analysis)
    
    print(f"\nMatched Rules Length: {len(matched)} characters")
    print(f"Sections: {len(matched.split('---'))}")
    print("\nFirst 500 characters of matched rules:")
    print(matched[:500])
    print("...")

if __name__ == "__main__":
    print("Rajanadi Astrology Backend Test")
    print("=" * 50)
    
    try:
        # Test chart calculation
        natal, navamsa = test_chart_calculation()
        
        # Test Rajanadi engine
        analysis = test_rajanadi_engine(natal, navamsa)
        
        # Test pattern matching
        test_rules_matcher(analysis)
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start Ollama: ollama serve")
        print("3. Run API: uvicorn app.main:app --reload")
        print("4. Visit: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

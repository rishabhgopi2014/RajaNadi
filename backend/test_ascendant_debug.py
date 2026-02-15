"""
Test ascendant calculation for debugging
Compare calculated position with expected position from original horoscope
"""
from app.services.chart_calculator import chart_calculator
import json

# Test Case 1: 1979-10-14, 23:23:00, Tiruchirappalli
print("=" * 70)
print("TEST CASE 1: 1979-10-14, 23:23:00, Tiruchirappalli")
print("=" * 70)
print("Expected: Ascendant in House 3 (Gemini)")
print()

result1 = chart_calculator.calculate_natal_chart(
    year=1979, 
    month=10, 
    day=14, 
    hour=23, 
    minute=23, 
    second=0, 
    latitude=10.7905,  # Tiruchirappalli coordinates
    longitude=78.7047
)

asc1 = result1['Ascendant']
print(f"Calculated Ascendant:")
print(f"  Rasi: {asc1['rasi']} ({asc1['rasi_name']})")
print(f"  Longitude: {asc1['longitude']:.4f}°")
print(f"  Degree in sign: {asc1['degree']:.2f}°")
print(f"  Expected: House 3 (Gemini)")
print(f"  Match: {'✓ YES' if asc1['rasi'] == 3 else '✗ NO'}")
print()

# Calculate what correction would be needed
if asc1['rasi'] != 3:
    current_lon = asc1['longitude']
    # Gemini is houses 3, so longitude should be 60-90 degrees
    gemini_start = 60
    gemini_end = 90
    
    # Find the correction needed
    if current_lon < gemini_start:
        correction_needed = gemini_start - current_lon
        direction = "add"
    elif current_lon > gemini_end:
        # Calculate shortest path
        correction_needed = current_lon - gemini_end
        direction = "subtract"
    else:
        correction_needed = 0
        direction = "none"
    
    print(f"ANALYSIS:")
    print(f"  Current longitude: {current_lon:.2f}°")
    print(f"  Gemini range: {gemini_start}° - {gemini_end}°")
    print(f"  Correction needed: {direction} {abs(correction_needed):.2f}°")
    print()

# Test Case 2: 1983-08-08, 04:30:00, Chennai (from old test)
print("=" * 70)
print("TEST CASE 2: 1983-08-08, 04:30:00, Chennai")
print("=" * 70)
print("Expected: Ascendant in House 4 (Cancer) - from test file")
print()

result2 = chart_calculator.calculate_natal_chart(
    year=1983, 
    month=8, 
    day=8, 
    hour=4, 
    minute=30, 
    second=0, 
    latitude=13.0827,  # Chennai coordinates
    longitude=80.2707
)

asc2 = result2['Ascendant']
print(f"Calculated Ascendant:")
print(f"  Rasi: {asc2['rasi']} ({asc2['rasi_name']})")
print(f"  Longitude: {asc2['longitude']:.4f}°")
print(f"  Degree in sign: {asc2['degree']:.2f}°")
print(f"  Expected: House 4 (Cancer)")
print(f"  Match: {'✓ YES' if asc2['rasi'] == 4 else '✗ NO'}")
print()

# Save results
output = {
    "test_case_1": {
        "birth_details": "1979-10-14 23:23:00 Tiruchirappalli",
        "calculated_rasi": asc1['rasi'],
        "calculated_name": asc1['rasi_name'],
        "longitude": round(asc1['longitude'], 4),
        "degree": round(asc1['degree'], 2),
        "expected_rasi": 3,
        "expected_name": "Gemini",
        "match": asc1['rasi'] == 3
    },
    "test_case_2": {
        "birth_details": "1983-08-08 04:30:00 Chennai",
        "calculated_rasi": asc2['rasi'],
        "calculated_name": asc2['rasi_name'],
        "longitude": round(asc2['longitude'], 4),
        "degree": round(asc2['degree'], 2),
        "expected_rasi": 4,
        "expected_name": "Cancer",
        "match": asc2['rasi'] == 4
    }
}

with open('ascendant_debug_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("=" * 70)
print("Results saved to ascendant_debug_results.json")
print("=" * 70)

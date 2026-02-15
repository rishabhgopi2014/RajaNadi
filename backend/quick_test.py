import sys
sys.path.insert(0, '.')
from app.services.chart_calculator import chart_calculator

# Test 1979-10-14, 23:23:00, Tiruchirappalli
r = chart_calculator.calculate_natal_chart(
    1979, 10, 14, 23, 23, 0,
    10.7905, 78.7047
)

asc = r['Ascendant']
print(f"Current: Rasi {asc['rasi']} ({asc['rasi_name']}), Lon: {asc['longitude']:.2f}")
print(f"Expected: Rasi 3 (Gemini)")
print(f"Match: {asc['rasi'] == 3}")

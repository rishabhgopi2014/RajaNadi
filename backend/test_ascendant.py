from app.services.chart_calculator import chart_calculator
import json

# Test ascendant calculation for 1983-08-08, 04:30:00, Chennai
result = chart_calculator.calculate_natal_chart(
    year=1983, 
    month=8, 
    day=8, 
    hour=4, 
    minute=30, 
    second=0, 
    latitude=13.0827, 
    longitude=80.2707
)

asc = result['Ascendant']

output = {
    "ascendant": {
        "rasi": asc['rasi'],
        "rasi_name": asc['rasi_name'],
        "longitude": round(asc['longitude'], 4),
        "degree": round(asc['degree'], 2)
    },
    "expected": "Rasi 4 (Cancer)",
    "match": asc['rasi'] == 4
}

print(json.dumps(output, indent=2))

with open('ascendant_test_result.json', 'w') as f:
    json.dump(output, f, indent=2)
    
print(f"\nResult saved to ascendant_test_result.json")

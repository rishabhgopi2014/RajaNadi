# Retrograde Planets - Comprehensive Guide

Understanding how retrograde planets are calculated, displayed, and influence predictions in RajanadiAstro.

## What is Retrograde Motion?

In Vedic astrology, a planet is **retrograde** when it appears to move backward through the zodiac from Earth's perspective. This is an optical illusion caused by relative orbital speeds.

### Astrological Significance

Retrograde planets:
- **Amplify influence** - Stronger effects on life areas they govern
- **Internalize energy** - Effects felt more internally than externally  
- **Delay results** - Outcomes may be postponed or require reworking
- **Review and revision** - Periods for reflection and reassessment

## Technical Implementation

### Backend Calculation

**File**: `backend/app/services/chart_calculator.py`

```python
# Line ~135
speed = planet_vel.km_per_s
is_retro = speed[0] < 0  # Negative velocity = retrograde

planets_data[name] = {
    'longitude': lon_sidereal,
    'rasi': rasi,
    'degree': degree,
    'is_retrograde': is_retro,
    'speed': round(speed[0], 6)
}
```

**Detection Method**: 
- Uses Skyfield's velocity calculation
- Negative velocity in ecliptic longitude = retrograde
- Checked for: Mercury, Venus, Mars, Jupiter, Saturn
- **Never retrograde**: Sun, Moon, Rahu, Ketu, Ascendant

### Data Model

**File**: `backend/app/models/chart_data.py`

```python
class PlanetData(BaseModel):
    rasi: int
    rasi_name: str
    degree: float
    longitude: float
    is_retrograde: bool  # Boolean flag
    speed: float  # km/s in ecliptic longitude
```

## Visual Indicators

### 1. South Indian Chart (Visual)

**Display**: `℞` symbol next to planet abbreviation

**Example**:
```
Box 4: Mo Ma℞  
       (Moon and Mars, Mars is retrograde)
```

**File**: `frontend/src/components/SouthIndianChart.jsx`

```jsx
const planetLabel = data.is_retrograde 
    && planet !== 'Ascendant' 
    && planet !== 'Rahu' 
    && planet !== 'Ketu'
    ? `${shortName}℞`
    : shortName
```

### 2. Planet Details Tables

**Display**: Red "R" badge next to planet name

**Styling**:
- Background: `rgba(239, 68, 68, 0.2)`
- Color: `#ef4444` (red)
- Border: `1px solid #ef4444`
- Font: Bold, small

**Example**:
```
Mercury [R]  Gemini  15.3°
```

**File**: `frontend/src/components/ChartsPage.jsx`

```jsx
<span className="planet-name">
    {planet}
    {data.is_retrograde && <span className="retrograde-badge">R</span>}
</span>
```

## Retrograde in Predictions

### 1. Authority Planet Selection

**Highest Priority**: Retrograde planets are checked FIRST

**File**: `backend/app/services/rajanadi_engine.py`

```python
def identify_authority_planet(self, planets: Dict) -> Optional[str]:
    # Priority 1: Retrograde planets
    retrogrades = [name for name, data in planets.items() 
                  if data.get('is_retrograde', False) 
                  and name not in ['Ascendant', 'Rahu', 'Ketu']]
    if retrogrades:
        return retrogrades[0]  # First retrograde = Authority
    
    # Priority 2: Edge planets (0-2° or 28-30°)
    # Priority 3: Exalted/Debilitated
    # ...
```

**Rationale**: Raja Nadi principle - retrograde planets wield strongest influence.

### 2. AI Prediction Prompts

**Retrograde Status Included**: Yes

**File**: `backend/app/services/ollama_service.py`

```python
# Line ~27
natal_info = []
for name, data in planets.items():
    retro = " (R)" if data.get('is_retrograde') else ""
    natal_info.append(
        f"- {name}{retro}: {data['rasi_name']} {data['degree']:.1f}°"
    )

# Line ~38
if data['is_retrograde']:
    retrograde_planets.append(name)

# Included in prompt
f"Retrograde Planets: {', '.join(retrograde_planets)}"
```

**AI Instructions**: The AI is explicitly told:
- Which planets are retrograde
- To consider retrograde effects in predictions
- To mention retrograde significance if relevant

## Retrograde Periods (2026)

**Display Format**: Comprehensive table on Charts page

| Planet | Retrograde Begins | Retrograde Ends | Signs |
|--------|------------------|-----------------|-------|
| Mercury | Feb 26 | Mar 20 | Pisces |
| Mercury | Jun 29 | Jul 24 | Cancer/Gemini |
| Mercury | Oct 24 | Nov 13 | Scorpio/Libra |
| Venus | Oct 3 | Nov 14 | Scorpio/Libra |
| Jupiter | (From 2025) | Mar 11 | Cancer |
| Jupiter | Dec 13 | (Into 2027) | Leo |
| Saturn | Jul 27 | Dec 11 | Pisces/Aries |

**Source**: `backend/app/services/comprehensive_transit_service.py`

## Planet-Specific Effects

### Mercury Retrograde
- **Communication delays** - Misunderstandings, tech issues
- **Travel disruptions** - Plan ahead
- **Review contracts** - Don't sign new agreements
- **Reconnect with past** - Old friends, revisit ideas

### Venus Retrograde
- **Relationship review** - Reassess partnerships
- **Financial caution** - Avoid major purchases
- **Beauty/aesthetics** - Reconsider style changes
- **Past loves** - May resurface

### Mars Retrograde
- **Energy dips** - Avoid starting new projects
- **Anger management** -conflicts more likely
- **Sexual energy** - May feel muted
- **Revisit abandoned goals** - Finish old projects

### Jupiter Retrograde
- **Spiritual growth** - Internal expansion
- **Educational review** - Consolidate learning
- **Financial reassessment** - Review investments
- **Philosophical questioning** - Examine beliefs

### Saturn Retrograde
- **Karmic lessons** - Face responsibilities
- **Structure review** - Reassess commitments
- **Authority issues** - Challenge structures
- **Hard work pays off** - Delayed rewards manifest

## FAQ

### Q: Why don't Rahu and Ketu show retrograde?

**A**: Rahu and Ketu are always retrograde (moving backward through the zodiac). It's their natural motion, so marking them "R" would be redundant.

### Q: Can the Sun or Moon be retrograde?

**A**: No. The Sun and Moon never go retrograde from Earth's perspective.

### Q: How accurate is retrograde detection?

**A**: Very accurate. Skyfield uses JPL ephemeris data (NASA), accurate to within seconds of arc.

### Q: Does retrograde affect the Navamsa chart?

**A**: Yes. If a planet is retrograde in the natal chart, it's retrograde in all divisional charts (D9, D10, etc.).

### Q: Why is my Authority Planet retrograde?

**A**: Retrograde planets get TOP priority in Authority Planet selection. This amplifies their influence on your life path.

## Debugging Retrograde Issues

### Check if Planet is Retrograde

**Backend Test**:
```python
# test_backend.py
natal = chart_calculator.calculate_natal_chart(
    1983, 8, 8, 4, 30, 0, 13.0827, 80.2707
)
for planet, data in natal.items():
    if data['is_retrograde']:
        print(f"{planet} is retrograde: speed = {data['speed']}")
```

**Frontend Console**:
```javascript
console.log(chartData.natal.Mercury.is_retrograde)  // true/false
```

### Verify Visual Display

1. Open Charts page
2. Look for `℞` in South Indian chart boxes
3. Check for red "R" badges in details tables
4. Inspect element to verify CSS class `retrograde-badge`

## Related Documentation

- [Chart Calculation](chart-calculation.md) - How natal charts are generated
- [Raja Nadi Rules](../advanced/rajanadi-rules.md) - Authority planet logic
- [API Reference](..api/README.md#post-apicalculate-chart) - Chart endpoint details

---

**Key Takeaway**: Retrograde planets are fully integrated into RajanadiAstro - from calculation to display to prediction influence. The red "R" badge and ℞ symbol make them immediately visible, and the Authority Planet logic ensures their amplified significance is respected.

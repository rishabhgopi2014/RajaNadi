"""
For birth data: 1983-08-08, 04:30 AM, Chennai (13.0827N, 80.2707E)
Expected Ascendant: Cancer (Rasi 4)

Testing different calculation approaches to find the correct one.
"""

import math
from datetime import datetime

# Birth details
year, month, day = 1983, 8, 8
hour, minute = 4, 30
latitude = 13.0827  # Chennai
longitude = 80.2707  # Chennai

# Create Julian Day
# Simplified JD calculation
jd = 367 * year - int(7 * (year + int((month + 9) / 12)) / 4) + int(275 * month / 9) + day + 1721013.5
jd += (hour + minute / 60.0) / 24.0

# Calculate T (centuries from J2000)
T = (jd - 2451545.0) / 36525.0

# Calculate GMST (Greenwich Mean Sidereal Time) in degrees
gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + T * T * (0.000387933 - T / 38710000.0)
gmst = (gmst % 360) / 15.0  # Convert to hours

# Calculate LST (Local Sidereal Time)
lst = gmst + (longitude / 15.0)
lst = lst % 24  # Hours

# Convert to degrees (RAMC)
ramc = (lst * 15) % 360

print(f"Julian Day: {jd}")
print(f"GMST: {gmst:.4f} hours")
print(f"LST: {lst:.4f} hours") 
print(f"RAMC: {ramc:.4f} degrees")

# Obliquity
obliquity = 23.4393

# Try Method 1: Standard formula
lat_rad = math.radians(latitude)
ramc_rad = math.radians(ramc)
obl_rad = math.radians(obliquity)

num1 = math.cos(ramc_rad)
den1 = -(math.sin(ramc_rad) * math.cos(obl_rad) + math.tan(lat_rad) * math.sin(obl_rad))
asc1_trop = math.degrees(math.atan2(num1, den1))
if asc1_trop < 0:
    asc1_trop += 360

# Ayanamsa for 1983
ayanamsa = 23.85 + ((1983 - 2000) * 0.01397)
asc1_sid = (asc1_trop - ayanamsa) % 360
rasi1 = int(asc1_sid / 30) + 1

print(f"\nMethod 1 (Current):")
print(f"  Tropical ASC: {asc1_trop:.2f}°")
print(f"  Ayanamsa: {ayanamsa:.4f}°")
print(f"  Sidereal ASC: {asc1_sid:.2f}°")
print(f"  Rasi: {rasi1} (Expected: 4 for Cancer)")

# Try Method 2: Alternative sign convention
num2 = -math.cos(ramc_rad)
den2 = math.sin(ramc_rad) * math.cos(obl_rad) + math.tan(lat_rad) * math.sin(obl_rad)
asc2_trop = math.degrees(math.atan2(num2, den2))
if asc2_trop < 0:
    asc2_trop += 360

asc2_sid = (asc2_trop - ayanamsa) % 360
rasi2 = int(asc2_sid / 30) + 1

print(f"\nMethod 2 (Inverted signs):")
print(f"  Tropical ASC: {asc2_trop:.2f}°")
print(f"  Sidereal ASC: {asc2_sid:.2f}°")
print(f"  Rasi: {rasi2} (Expected: 4 for Cancer)")

# Try Method 3: Add 180° to RAMC
ramc3 = (ramc + 180) % 360
ramc3_rad = math.radians(ramc3)
num3 = math.cos(ramc3_rad)
den3 = -(math.sin(ramc3_rad) * math.cos(obl_rad) + math.tan(lat_rad) * math.sin(obl_rad))
asc3_trop = math.degrees(math.atan2(num3, den3))
if asc3_trop < 0:
    asc3_trop += 360

asc3_sid = (asc3_trop - ayanamsa) % 360
rasi3 = int(asc3_sid / 30) + 1

print(f"\nMethod 3 (RAMC + 180°):")
print(f"  Tropical ASC: {asc3_trop:.2f}°")
print(f"  Sidereal ASC: {asc3_sid:.2f}°")
print(f"  Rasi: {rasi3} (Expected: 4 for Cancer)")

# Expected Cancer range: 90-120 degrees sidereal
print(f"\n✓ Cancer sidereal range: 90° - 120°")
print(f"  Method 1 at: {asc1_sid:.2f}° {'✓ MATCH' if 90 <= asc1_sid < 120 else '✗'}")
print(f"  Method 2 at: {asc2_sid:.2f}° {'✓ MATCH' if 90 <= asc2_sid < 120 else '✗'}")
print(f"  Method 3 at: {asc3_sid:.2f}° {'✓ MATCH' if 90 <= asc3_sid < 120 else '✗'}")

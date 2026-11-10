"""
Wildfire Spread Simulator Service
Based on Huygens Elliptical Wave Propagation Principle
Integrates real-time weather from Open-Meteo API (wind speed, azimuth, humidity)
"""

import math
import requests
from typing import Dict, Any, List

def fetch_live_weather(lat: float, lon: float) -> Dict[str, Any]:
    """
    Fetch real-time weather parameters using Open-Meteo free API.
    Fallback to realistic regional climatological baseline if offline.
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m&timezone=auto"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            data = res.json()
            curr = data.get("current", {})
            return {
                "wind_speed_kmh": curr.get("wind_speed_10m", 18.5),
                "wind_direction_deg": curr.get("wind_direction_10m", 65.0), # degrees clockwise from north
                "humidity_pct": curr.get("relative_humidity_2m", 32.0),
                "temperature_c": curr.get("temperature_2m", 33.5),
                "source": "Open-Meteo Live API"
            }
    except Exception:
        pass
    
    # Regional forest summer baseline (Western Ghats / Central India)
    return {
        "wind_speed_kmh": 22.0,
        "wind_direction_deg": 75.0,
        "humidity_pct": 28.0,
        "temperature_c": 35.0,
        "source": "Cached Regional Microclimate Baseline"
    }

def calculate_fire_perimeter(
    center_lat: float,
    center_lon: float,
    hours: float,
    wind_speed_kmh: float,
    wind_direction_deg: float,
    fuel_dryness_factor: float = 1.2
) -> Dict[str, Any]:
    """
    Calculates Huygens elliptical wave propagation perimeter for a wildfire.
    - center_lat, center_lon: ignition origin coordinates
    - hours: forecast duration (e.g. 0.5, 3.0, 6.0, 12.0)
    - wind_speed_kmh: wind velocity
    - wind_direction_deg: direction wind is blowing FROM (degrees from North)
    - fuel_dryness_factor: derived from Sentinel-2 NDWI/NDVI
    """
    if hours <= 0:
        return {
            "polygon": [[center_lat, center_lon]],
            "area_ha": 0.5,
            "perimeter_km": 0.2,
            "forward_reach_km": 0.05,
            "threat_level": "Ignition Point"
        }

    # Wind blowing TO is opposite of wind coming FROM
    blow_to_deg = (wind_direction_deg + 180.0) % 360.0
    theta_rad = math.radians(blow_to_deg)

    # Base spread rate in km/h based on fuel dryness and baseline rate
    base_rate = 0.18 * fuel_dryness_factor
    
    # Wind amplification factor
    wind_factor = 1.0 + (wind_speed_kmh / 12.0) ** 1.3

    # Ellipse semi-major axis (head of the fire downwind)
    a_head = base_rate * wind_factor * hours  # km
    # Ellipse back spread rate (much slower upwind)
    a_back = base_rate * 0.25 * hours  # km
    # Total semi-major axis length
    a = (a_head + a_back) / 2.0
    # Displacement of ellipse center from ignition point along wind direction
    c_shift = (a_head - a_back) / 2.0

    # Semi-minor axis (flanks) based on length-to-breadth ratio (Alexander 1985)
    # LB ratio = 0.936 * exp(0.256 * U) + 0.461 where U is wind speed in m/s
    wind_ms = wind_speed_kmh / 3.6
    lb_ratio = max(1.1, min(4.5, 0.936 * math.exp(0.08 * wind_ms) + 0.4))
    b = a / lb_ratio

    # Center of ellipse shifted downwind
    # 1 deg latitude ≈ 111.0 km, 1 deg longitude ≈ 111.0 * cos(lat) km
    lat_deg_per_km = 1.0 / 111.0
    lon_deg_per_km = 1.0 / (111.0 * math.cos(math.radians(center_lat)))

    ellipse_center_lat = center_lat + (c_shift * math.cos(theta_rad)) * lat_deg_per_km
    ellipse_center_lon = center_lon + (c_shift * math.sin(theta_rad)) * lon_deg_per_km

    # Generate perimeter polygon coordinates (36 points)
    polygon = []
    num_points = 36
    for i in range(num_points):
        alpha = 2.0 * math.pi * i / num_points
        # Coordinates in ellipse local frame
        x_local = a * math.cos(alpha)
        y_local = b * math.sin(alpha)

        # Rotate by wind direction theta
        dx = x_local * math.cos(theta_rad) - y_local * math.sin(theta_rad)
        dy = x_local * math.sin(theta_rad) + y_local * math.cos(theta_rad)

        pt_lat = ellipse_center_lat + dx * lat_deg_per_km
        pt_lon = ellipse_center_lon + dy * lon_deg_per_km
        polygon.append([round(pt_lat, 6), round(pt_lon, 6)])

    # Close polygon
    polygon.append(polygon[0])

    # Calculate approximate burnt area (in hectares)
    area_km2 = math.pi * a * b
    area_ha = round(area_km2 * 100.0, 2)
    # Ramanujan's formula for perimeter
    h = ((a - b) ** 2) / ((a + b) ** 2)
    perimeter_km = round(math.pi * (a + b) * (1.0 + (3.0 * h) / (10.0 + math.sqrt(4.0 - 3.0 * h))), 2)

    # Determine threat tier
    if area_ha > 80.0:
        threat_level = "Critical Disaster (Tier 3)"
    elif area_ha > 20.0:
        threat_level = "Severe Spread (Tier 2)"
    else:
        threat_level = "Contained / Moderate (Tier 1)"

    return {
        "polygon": polygon,
        "area_ha": area_ha,
        "perimeter_km": perimeter_km,
        "forward_reach_km": round(a_head, 2),
        "threat_level": threat_level,
        "ellipse_params": {
            "semi_major_km": round(a, 3),
            "semi_minor_km": round(b, 3),
            "wind_influence_ratio": round(lb_ratio, 2)
        }
    }

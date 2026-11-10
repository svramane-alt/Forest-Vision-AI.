"""
Forest Vision AI (VanaRakshak) - Master Backend Server
PCCOE International Grand Challenge 2026 (Indradhanu)
Theme: AI for Climate Change
"""

import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from services.simulator import calculate_fire_perimeter, fetch_live_weather
from services.forensics import analyze_forest_patch
from services.compliance import check_parivesh_compliance
from services.carbon import calculate_carbon_and_reforestation

app = FastAPI(
    title="Forest Vision AI Backend",
    description="Predictive Wildfire Simulator, Forensics Intent Classifier, and PARIVESH Compliance API",
    version="1.0.0"
)

# In-memory realistic field incidents across Western Ghats & Maharashtra Protected Reserves
SAMPLE_INCIDENTS = [
    {
        "id": "INC-MH-2026-081",
        "title": "Koyna Sanctuary Ridge - Thermal Hotspot",
        "type": "WILDFIRE",
        "lat": 17.4125,
        "lon": 73.7482,
        "location_name": "Koyna Wildlife Sanctuary, Satara, Maharashtra",
        "detection_source": "NASA FIRMS (VIIRS S-NPP 375m)",
        "brightness_temp_k": 348.6,
        "frp_mw": 42.8, # Fire Radiative Power
        "ndvi_baseline": 0.78,
        "current_ndvi": 0.22,
        "fuel_dryness_factor": 1.45,
        "status": "ACTIVE_CRITICAL",
        "patch_metrics": {
            "area_ha": 14.8,
            "length_m": 620,
            "width_m": 240,
            "perimeter_m": 1850,
            "canopy_loss_pct": 82.0
        }
    },
    {
        "id": "INC-MH-2026-082",
        "title": "Western Ghats Corridor - Linear Canopy Loss",
        "type": "DEFORESTATION",
        "lat": 17.9150,
        "lon": 73.5820,
        "location_name": "Mahad - Poladpur Forest Range, Raigad, Maharashtra",
        "detection_source": "Copernicus Sentinel-2 (B8 NIR / B4 Red)",
        "brightness_temp_k": 302.1,
        "frp_mw": 0.0,
        "ndvi_baseline": 0.82,
        "current_ndvi": 0.38,
        "fuel_dryness_factor": 1.10,
        "status": "INVESTIGATION_FLAGGED",
        "patch_metrics": {
            "area_ha": 6.4,
            "length_m": 1280,
            "width_m": 50,
            "perimeter_m": 2660,
            "canopy_loss_pct": 95.0
        }
    },
    {
        "id": "INC-MH-2026-083",
        "title": "Chandoli National Park Buffer - Rectangular Parcel Clearing",
        "type": "DEFORESTATION",
        "lat": 17.1520,
        "lon": 73.8560,
        "location_name": "Chandoli National Park Periphery, Sangli, Maharashtra",
        "detection_source": "Copernicus Sentinel-2 Cloud-Free Composite",
        "brightness_temp_k": 301.5,
        "frp_mw": 0.0,
        "ndvi_baseline": 0.74,
        "current_ndvi": 0.31,
        "fuel_dryness_factor": 1.15,
        "status": "SURVEY_PENDING",
        "patch_metrics": {
            "area_ha": 9.2,
            "length_m": 340,
            "width_m": 270,
            "perimeter_m": 1220,
            "canopy_loss_pct": 88.0
        }
    },
    {
        "id": "INC-MH-2026-084",
        "title": "Gadchiroli Reserve - Excavated Quarry Anomaly",
        "type": "DEFORESTATION",
        "lat": 20.1840,
        "lon": 80.0120,
        "location_name": "Allapalli Forest Division, Gadchiroli, Maharashtra",
        "detection_source": "Sentinel-2 & PlanetScope High-Res Tasking",
        "brightness_temp_k": 308.2,
        "frp_mw": 0.0,
        "ndvi_baseline": 0.85,
        "current_ndvi": 0.18,
        "fuel_dryness_factor": 1.30,
        "status": "CRITICAL_ACTION",
        "patch_metrics": {
            "area_ha": 12.5,
            "length_m": 410,
            "width_m": 305,
            "perimeter_m": 1490,
            "canopy_loss_pct": 96.5
        }
    }
]

# Request schemas
class FireSimulationRequest(BaseModel):
    center_lat: float
    center_lon: float
    hours: float = 3.0
    wind_speed_kmh: Optional[float] = None
    wind_direction_deg: Optional[float] = None
    fuel_dryness_factor: Optional[float] = 1.25

class ForensicsRequest(BaseModel):
    patch_id: str
    area_ha: float
    length_m: float
    width_m: float
    perimeter_m: float
    canopy_loss_pct: float
    spectral_ndvi_drop: float

class ComplianceRequest(BaseModel):
    lat: float
    lon: float

class CarbonRequest(BaseModel):
    area_ha: float
    ecosystem: Optional[str] = "Western_Ghats_Moist_Deciduous"


@app.get("/api/incidents")
def get_incidents():
    """Return catalog of active forest hotspot & clearing incidents."""
    return {"status": "success", "count": len(SAMPLE_INCIDENTS), "incidents": SAMPLE_INCIDENTS}

@app.get("/api/weather")
def get_weather(lat: float = Query(...), lon: float = Query(...)):
    """Fetch live or regional weather vectors for fire simulation."""
    weather = fetch_live_weather(lat, lon)
    return {"status": "success", "weather": weather}

@app.post("/api/simulate-fire")
def simulate_fire(req: FireSimulationRequest):
    """
    Simulates wildfire spread perimeter using Huygens elliptical model.
    Fetches live weather if wind vectors are not provided.
    """
    w_speed = req.wind_speed_kmh
    w_dir = req.wind_direction_deg
    weather_meta = None

    if w_speed is None or w_dir is None:
        weather_meta = fetch_live_weather(req.center_lat, req.center_lon)
        w_speed = weather_meta["wind_speed_kmh"]
        w_dir = weather_meta["wind_direction_deg"]

    sim_result = calculate_fire_perimeter(
        center_lat=req.center_lat,
        center_lon=req.center_lon,
        hours=req.hours,
        wind_speed_kmh=w_speed,
        wind_direction_deg=w_dir,
        fuel_dryness_factor=req.fuel_dryness_factor or 1.25
    )

    return {
        "status": "success",
        "simulation": sim_result,
        "meteorological_conditions": {
            "wind_speed_kmh": w_speed,
            "wind_direction_deg": w_dir,
            "hours_forecast": req.hours,
            "weather_source": weather_meta["source"] if weather_meta else "User Specified"
        }
    }

@app.post("/api/forensics-analysis")
def perform_forensics(req: ForensicsRequest):
    """Classifies patch geometry into illegal logging, agriculture, or mining."""
    result = analyze_forest_patch(
        patch_id=req.patch_id,
        area_ha=req.area_ha,
        length_m=req.length_m,
        width_m=req.width_m,
        perimeter_m=req.perimeter_m,
        canopy_loss_pct=req.canopy_loss_pct,
        spectral_ndvi_drop=req.spectral_ndvi_drop
    )
    return {"status": "success", "forensics": result}

@app.post("/api/compliance-check")
def perform_compliance(req: ComplianceRequest):
    """Checks coordinate against approved MoEFCC PARIVESH polygons."""
    result = check_parivesh_compliance(req.lat, req.lon)
    return {"status": "success", "compliance": result}

@app.post("/api/carbon-assessment")
def perform_carbon_assessment(req: CarbonRequest):
    """Calculates IPCC biomass & CO2 loss with native flora reforestation roadmap."""
    result = calculate_carbon_and_reforestation(req.area_ha, req.ecosystem)
    return {"status": "success", "carbon_impact": result}

@app.get("/api/incident/{incident_id}/complete-docket")
def get_incident_complete_docket(incident_id: str):
    """Assembles all 4 pillars into a formal Forest Range Officer Legal Docket."""
    incident = next((inc for inc in SAMPLE_INCIDENTS if inc["id"] == incident_id), None)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident ID not found")

    lat = incident["lat"]
    lon = incident["lon"]
    m = incident["patch_metrics"]

    # 1. Weather & fire simulation (6 hours forecast)
    weather = fetch_live_weather(lat, lon)
    fire_sim = calculate_fire_perimeter(
        center_lat=lat,
        center_lon=lon,
        hours=6.0,
        wind_speed_kmh=weather["wind_speed_kmh"],
        wind_direction_deg=weather["wind_direction_deg"],
        fuel_dryness_factor=incident["fuel_dryness_factor"]
    )

    # 2. Forensics diagnosis
    forensics = analyze_forest_patch(
        patch_id=incident["id"],
        area_ha=m["area_ha"],
        length_m=m["length_m"],
        width_m=m["width_m"],
        perimeter_m=m["perimeter_m"],
        canopy_loss_pct=m["canopy_loss_pct"],
        spectral_ndvi_drop=round(incident["ndvi_baseline"] - incident["current_ndvi"], 3)
    )

    # 3. PARIVESH compliance check
    compliance = check_parivesh_compliance(lat, lon)

    # 4. IPCC Carbon & Reforestation
    carbon = calculate_carbon_and_reforestation(m["area_ha"])

    return {
        "status": "success",
        "docket_id": f"DOCKET-{incident['id']}",
        "timestamp": "2026-10-08T11:45:00Z",
        "jurisdiction": "Maharashtra State Forest Department, Pune/Kolhapur Circle",
        "incident": incident,
        "meteorology": weather,
        "fire_forecast_6h": fire_sim,
        "ai_forensics": forensics,
        "parivesh_compliance": compliance,
        "ipcc_carbon_impact": carbon,
        "statutory_violation": "Indian Forest Act (1927) Section 26(1)(a) & Wildlife Protection Act (1972) Section 27",
        "recommended_enforcement": "Immediate seizure of machinery, register Preliminary Offence Report (POR), deploy drone inspection."
    }

# Mount static folder for frontend dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Forest Vision AI API running. Place index.html in static folder."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

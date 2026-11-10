"""
IPCC Carbon Sequestration Loss & AI Reforestation Recommendation Engine
Calculates lost vegetative biomass and CO2 equivalent release.
Recommends hyper-local indigenous species to restore native biodiverse canopy.
"""

from typing import Dict, Any, List

# Regional indigenous tree species database (Western Ghats & Central India)
REGIONAL_FLORA_DATABASE = [
    {
        "species_name": "Tectona grandis (Teak / Saag)",
        "canopy_type": "Deciduous Hardwood",
        "growth_rate": "Moderate (15-20 yrs)",
        "carbon_absorption_t_yr": 0.045, # ~45 kg CO2/tree/year
        "soil_suitability": "Well-drained alluvial and basaltic red loam",
        "ecological_role": "High canopy structural stability and biodiversity shelter"
    },
    {
        "species_name": "Dendrocalamus strictus (Solid Bamboo / Manvel)",
        "canopy_type": "Rapid Pioneer Biomass",
        "growth_rate": "Ultra-Fast (3-5 yrs)",
        "carbon_absorption_t_yr": 0.065, # ~65 kg CO2/clump/year
        "soil_suitability": "Erosion-prone slopes, riverbanks, degraded gravel",
        "ecological_role": "Immediate soil binding, prevents landslides, restores moisture retention"
    },
    {
        "species_name": "Syzygium cumini (Jamun)",
        "canopy_type": "Evergreen Fruit-Bearing",
        "growth_rate": "Moderate-Fast (8-12 yrs)",
        "carbon_absorption_t_yr": 0.050,
        "soil_suitability": "Moist valleys, riparian buffers, deep loam",
        "ecological_role": "Critical food source for hornbills, flying foxes, and native primates"
    },
    {
        "species_name": "Terminalia elliptica (Ain / Crocodile Bark Tree)",
        "canopy_type": "Dense Canopy Keystone",
        "growth_rate": "Moderate (12-18 yrs)",
        "carbon_absorption_t_yr": 0.058,
        "soil_suitability": "Heavy clay, moisture-retentive basaltic soil",
        "ecological_role": "Natural fire-resistant bark, water storage reservoir in trunk"
    }
]

def calculate_carbon_and_reforestation(area_ha: float, ecosystem: str = "Western_Ghats_Moist_Deciduous") -> Dict[str, Any]:
    """
    IPCC Tier 1 Greenhouse Gas Inventory Methodology:
    Carbon Stock Loss (tCO2e) = Area (ha) * AGB (150 t/ha) * Carbon Fraction (0.5) * (44 / 12)
    """
    avg_biomass_t_per_ha = 150.0 # Above Ground Biomass (t/ha) for tropical moist deciduous
    carbon_fraction = 0.50
    co2_conversion_factor = 44.0 / 12.0 # 3.667

    total_biomass_lost_tonnes = area_ha * avg_biomass_t_per_ha
    total_carbon_tonnes = total_biomass_lost_tonnes * carbon_fraction
    total_co2e_lost_tonnes = total_carbon_tonnes * co2_conversion_factor

    # Typical reforestation density: 1,100 saplings per hectare
    saplings_needed = int(round(area_ha * 1100))

    # Equivalent impact analogies
    car_km_equivalent = round(total_co2e_lost_tonnes * 4000.0) # ~4000 km driven per tCO2
    household_annual_power = round(total_co2e_lost_tonnes / 2.2) # ~2.2 tCO2 per rural household per year

    # 10-year carbon recovery projection assuming 85% survival rate
    annual_recapture_rate = saplings_needed * 0.85 * 0.052 # avg 52kg/tree
    recovery_years = round(total_co2e_lost_tonnes / max(annual_recapture_rate, 0.1), 1)

    return {
        "area_hectares": round(area_ha, 2),
        "biomass_lost_tonnes": round(total_biomass_lost_tonnes, 1),
        "carbon_lost_tonnes": round(total_carbon_tonnes, 1),
        "co2e_released_tonnes": round(total_co2e_lost_tonnes, 1),
        "impact_equivalencies": {
            "passenger_vehicles_annual_emissions": round(total_co2e_lost_tonnes / 4.6, 1),
            "household_yearly_energy_usage": household_annual_power,
            "vehicle_kilometers_driven": car_km_equivalent
        },
        "reforestation_prescription": {
            "total_saplings_required": saplings_needed,
            "planting_density": "1,100 stems/ha (Miyawaki + Social Forestry hybrid)",
            "estimated_recovery_time_years": recovery_years,
            "recommended_species": REGIONAL_FLORA_DATABASE
        }
    }

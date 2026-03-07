from pydantic import BaseModel
from typing import Optional


class RiskAssessment(BaseModel):
    plot_id: str
    drought_risk: float
    wildfire_risk: float
    deforestation_risk: float
    political_risk: float
    composite_risk: float
    weather_data: Optional[dict] = None


class RiskAssessmentResponse(RiskAssessment):
    id: str
    assessment_date: Optional[str] = None


class ScanRequest(BaseModel):
    plot_id: Optional[str] = None
    geometry: Optional[dict] = None  # GeoJSON Polygon
    owner_id: str


class ScanResponse(BaseModel):
    scan_id: str
    plot_id: Optional[str] = None
    mean_ndvi: float
    mean_evi: float
    estimated_biomass: float
    estimated_tco2e: float
    carbon_density: float
    integrity_score: float
    buy_price_per_tonne: float
    risk_adjustment: float
    raw_bands: Optional[dict] = None


class FootprintRequest(BaseModel):
    energy_kwh_monthly: float = 0
    fuel_litres_monthly: float = 0
    fuel_type: str = "diesel"
    flights_short_km_annual: float = 0  # Flights < 1500 km
    flights_long_km_annual: float = 0  # Flights > 1500 km
    waste_landfill_kg_monthly: float = 0
    waste_recycled_kg_monthly: float = 0
    water_m3_monthly: float = 0
    freight_tonne_km_monthly: float = 0
    industry_sector: Optional[str] = None


class FootprintResponse(BaseModel):
    annual_tco2e: float
    electricity_tco2e: float
    fuel_tco2e: float
    flights_tco2e: float
    waste_tco2e: float
    water_tco2e: float
    freight_tco2e: float
    monthly_tco2e: float
    breakdown: dict

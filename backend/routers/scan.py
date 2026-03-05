import uuid
from fastapi import APIRouter, HTTPException
from models.risk import ScanRequest, ScanResponse
from services.biomass_estimator import estimate_biomass, biomass_to_tco2e, calculate_integrity_score
from services.risk_scorer import calculate_risk_score, get_weather_data
from services.mock_data import generate_mock_bands, calculate_ndvi, calculate_evi, get_terrain_data
from services.carbon_calculator import calculate_credit_price
from database import get_supabase_client
import random

router = APIRouter(prefix="/api/scan", tags=["scan"])


@router.post("", response_model=ScanResponse)
async def run_scan(request: ScanRequest):
    db = get_supabase_client()

    # Get plot details if plot_id provided
    plot = None
    if request.plot_id:
        result = db.table("land_plots").select("*").eq("id", request.plot_id).execute()
        if result.data:
            plot = result.data[0]

    land_use = plot["land_use"] if plot else "forest"
    region = plot.get("region", "Nyeri") if plot else "Nyeri"
    area = plot["area_hectares"] if plot else 10.0

    # Generate mock satellite bands
    bands = generate_mock_bands(land_use)
    ndvi = calculate_ndvi(bands)
    evi = calculate_evi(bands)

    # Get terrain data
    terrain = get_terrain_data(region)

    # Estimate biomass
    biomass = estimate_biomass(
        ndvi=ndvi,
        evi=evi,
        elevation=terrain["elevation"],
        slope=terrain["slope"],
        precip=terrain["precip"],
        land_use=land_use,
    )

    # Calculate tCO2e
    tco2e = biomass_to_tco2e(biomass, area)
    carbon_density = round(tco2e / area, 2) if area > 0 else 0

    # Risk assessment
    weather = get_weather_data(region)
    risk = calculate_risk_score(weather, land_use)

    # Integrity score
    integrity = calculate_integrity_score(
        ndvi_mean=ndvi,
        ndvi_std=random.uniform(0.02, 0.15),
        temporal_ndvi_change=random.uniform(-0.05, 0.1),
        cloud_cover_pct=random.uniform(5, 30),
        scan_resolution_m=10.0,
        biomass_model_r2=random.uniform(0.82, 0.95),
        drought_risk=risk["drought_risk"],
        wildfire_risk=risk["wildfire_risk"],
        deforestation_proximity_km=random.uniform(5, 40),
        years_under_conservation=random.uniform(0, 15),
        land_use=land_use,
        additionality_score=random.uniform(0.4, 0.9),
    )

    # Price
    price = calculate_credit_price(integrity, risk["composite_risk"])

    # Save scan result to DB
    scan_id = str(uuid.uuid4())
    scan_record = {
        "id": scan_id,
        "plot_id": request.plot_id,
        "mean_ndvi": ndvi,
        "mean_evi": evi,
        "estimated_biomass": biomass,
        "estimated_tco2e": tco2e,
        "carbon_density": carbon_density,
        "integrity_score": integrity,
        "model_version": "rf_v1",
        "raw_bands": bands,
    }
    try:
        db.table("scan_results").insert(scan_record).execute()
    except Exception:
        pass  # Don't fail scan if DB insert fails

    return ScanResponse(
        scan_id=scan_id,
        plot_id=request.plot_id,
        mean_ndvi=ndvi,
        mean_evi=evi,
        estimated_biomass=biomass,
        estimated_tco2e=tco2e,
        carbon_density=carbon_density,
        integrity_score=integrity,
        buy_price_per_tonne=price,
        risk_adjustment=risk["composite_risk"],
        raw_bands=bands,
    )


@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    db = get_supabase_client()
    result = db.table("scan_results").select("*").eq("id", scan_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Scan not found")
    return result.data[0]

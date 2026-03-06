import uuid
import logging
from fastapi import APIRouter, HTTPException
from models.risk import ScanRequest, ScanResponse
from services.biomass_estimator import predict_biomass_from_features, biomass_to_tco2e, calculate_integrity_score
from services.risk_scorer import calculate_risk_score, get_weather_data
from services.gee_feature_extractor import extract_sentinel_features
from services.carbon_calculator import calculate_credit_price
from database import get_supabase_client
import random

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/scan", tags=["scan"])


@router.post("", response_model=ScanResponse)
async def run_scan(request: ScanRequest):
    logger.info(f"Processing scan request for owner: {request.owner_id}")
    
    # Convert "demo-user" string to proper UUID
    DEMO_USER_UUID = "00000000-0000-0000-0000-000000000001"
    owner_id = DEMO_USER_UUID if request.owner_id == "demo-user" else request.owner_id
    
    # Try to get plot details from database if available
    plot = None
    try:
        db = get_supabase_client()
        if request.plot_id:
            result = db.table("land_plots").select("*").eq("id", request.plot_id).execute()
            if result.data:
                plot = result.data[0]
                logger.info(f"Found plot {request.plot_id} in database")
    except Exception as e:
        # Database not configured, use defaults
        logger.warning(f"Database not available: {e}")

    land_use = plot["land_use"] if plot else "forest"
    region = plot.get("region", "Nyeri") if plot else "Nyeri"
    area = plot["area_hectares"] if plot else 10.0
    
    # Extract real Sentinel-2 features from Google Earth Engine
    if not request.geometry:
        raise HTTPException(status_code=400, detail="Geometry is required for scan")
    
    logger.info(f"Extracting Sentinel-2 features for geometry type: {request.geometry['type']}")
    features = extract_sentinel_features(
        geometry=request.geometry,
        start_date="2023-01-01",
        end_date="2024-12-31"
    )
    
    if features is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract satellite features. Check geometry and try again."
        )
    
    # Predict biomass using trained model
    biomass = predict_biomass_from_features(features)
    logger.info(f"Predicted biomass: {biomass} tonnes/ha")

    
    # Calculate tCO2e
    tco2e = biomass_to_tco2e(biomass, area)
    carbon_density = round(tco2e / area, 2) if area > 0 else 0

    # Risk assessment
    weather = get_weather_data(region)
    risk = calculate_risk_score(weather, land_use)

    # Integrity score
    ndvi = features['ndvi']
    evi = features['evi']
    integrity = calculate_integrity_score(
        ndvi_mean=ndvi,
        ndvi_std=random.uniform(0.02, 0.15),
        temporal_ndvi_change=random.uniform(-0.05, 0.1),
        cloud_cover_pct=random.uniform(5, 30),
        scan_resolution_m=10.0,
        biomass_model_r2=0.51,  # Test R² from model training
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
    
    # Build raw bands dict from features
    raw_bands = {
        'B2': features['blue'],
        'B3': features['green'],
        'B4': features['red'],
        'B8': features['nir'],
        'B11': features['swir1'],
        'B12': features['swir2'],
        'NDVI': features['ndvi'],
        'EVI': features['evi'],
        'elevation': features['elevation'],
        'slope': features['slope'],
        'n_images': features['n_images']
    }
    
    scan_record = {
        "id": scan_id,
        "plot_id": request.plot_id,
        "mean_ndvi": ndvi,
        "mean_evi": evi,
        "estimated_biomass": biomass,
        "estimated_tco2e": tco2e,
        "carbon_density": carbon_density,
        "integrity_score": integrity,
        "model_version": "biomass_model_v1",
        "raw_bands": raw_bands,
    }
    try:
        db = get_supabase_client()
        db.table("scan_results").insert(scan_record).execute()
        logger.info(f"Saved scan result {scan_id} to database")
        
        # Automatically create carbon credit from scan result
        credit_id = str(uuid.uuid4())
        credit_record = {
            "id": credit_id,
            "scan_id": scan_id,
            "plot_id": request.plot_id,
            "owner_id": owner_id,  # Use converted UUID
            "vintage_year": 2024,
            "quantity_tco2e": tco2e,
            "price_per_tonne": price,
            "status": "listed",  # Automatically list the credit
            "integrity_score": integrity,
            "risk_score": risk["composite_risk"] * 100,  # Convert to percentage
        }
        db.table("carbon_credits").insert(credit_record).execute()
        logger.info(f"Created carbon credit {credit_id} from scan {scan_id}")
        
    except Exception as e:
        logger.warning(f"Failed to save scan to DB: {e}")

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
        raw_bands=raw_bands,
    )


@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    db = get_supabase_client()
    result = db.table("scan_results").select("*").eq("id", scan_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Scan not found")
    return result.data[0]

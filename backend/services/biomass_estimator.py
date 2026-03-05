import joblib
import numpy as np
import os

_biomass_model = None
_integrity_model = None

LAND_USE_ENCODING = {
    "forest": 0,
    "agroforestry": 1,
    "grassland": 2,
    "cropland": 3,
    "wetland": 4,
}


def _load_biomass_model():
    global _biomass_model
    if _biomass_model is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")
        if os.path.exists(model_path):
            _biomass_model = joblib.load(model_path)
    return _biomass_model


def _load_integrity_model():
    global _integrity_model
    if _integrity_model is None:
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "ml", "integrity_model.pkl"
        )
        if os.path.exists(model_path):
            _integrity_model = joblib.load(model_path)
    return _integrity_model


def biomass_to_tco2e(biomass_tonnes_per_ha: float, area_hectares: float) -> float:
    carbon_fraction = 0.47  # IPCC default
    co2_ratio = 3.667  # 44/12
    tco2e_per_ha = biomass_tonnes_per_ha * carbon_fraction * co2_ratio
    return round(tco2e_per_ha * area_hectares, 2)


def estimate_biomass(
    ndvi: float,
    evi: float,
    elevation: float,
    slope: float,
    precip: float,
    land_use: str,
) -> float:
    model = _load_biomass_model()
    land_type = LAND_USE_ENCODING.get(land_use, 2)

    if model is not None:
        features = np.array([[ndvi, evi, elevation, slope, precip, land_type]])
        prediction = model.predict(features)[0]
        return round(float(np.clip(prediction, 5, 350)), 2)

    # Fallback formula if model not trained yet
    biomass = ndvi * 300 + evi * 50 + (precip - 800) / 1200 * 40 - slope * 0.5
    return round(float(np.clip(biomass, 5, 350)), 2)


def calculate_integrity_score(
    ndvi_mean: float,
    ndvi_std: float,
    temporal_ndvi_change: float,
    cloud_cover_pct: float,
    scan_resolution_m: float,
    biomass_model_r2: float,
    drought_risk: float,
    wildfire_risk: float,
    deforestation_proximity_km: float,
    years_under_conservation: float,
    land_use: str,
    additionality_score: float,
) -> float:
    model = _load_integrity_model()
    land_type = LAND_USE_ENCODING.get(land_use, 2)

    if model is not None:
        features = np.array(
            [
                [
                    ndvi_mean,
                    ndvi_std,
                    temporal_ndvi_change,
                    cloud_cover_pct,
                    scan_resolution_m,
                    biomass_model_r2,
                    drought_risk,
                    wildfire_risk,
                    deforestation_proximity_km,
                    years_under_conservation,
                    land_type,
                    additionality_score,
                ]
            ]
        )
        score = model.predict(features)[0]
        return round(float(np.clip(score, 0, 100)), 1)

    # Fallback rule-based calculation
    data_quality = (
        min(ndvi_mean / 0.8, 1.0) * 15
        + max(0, 1 - ndvi_std / 0.2) * 5
        + max(0, 1 - cloud_cover_pct / 100) * 5
        + max(0, 1 - scan_resolution_m / 60) * 5
    )
    model_conf = biomass_model_r2 * 20
    temporal = (
        max(0, 1 - abs(temporal_ndvi_change) / 0.3) * 10
        + min(years_under_conservation / 10, 1.0) * 10
    )
    risk_adj = (
        (1 - drought_risk) * 5
        + (1 - wildfire_risk) * 5
        + min(deforestation_proximity_km / 30, 1.0) * 5
    )
    additionality = additionality_score * 15
    score = data_quality + model_conf + temporal + risk_adj + additionality
    return round(float(np.clip(score, 0, 100)), 1)

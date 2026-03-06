import joblib
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

_biomass_model_data = None
_integrity_model = None

LAND_USE_ENCODING = {
    "forest": 0,
    "agroforestry": 1,
    "grassland": 2,
    "cropland": 3,
    "wetland": 4,
}


def _load_biomass_model():
    """Load the trained biomass model with scaler."""
    global _biomass_model_data
    if _biomass_model_data is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "biomass_model_v1.pkl")
        if os.path.exists(model_path):
            _biomass_model_data = joblib.load(model_path)
            logger.info(f"Loaded biomass model v1 (Test R²={_biomass_model_data.get('test_r2', 'N/A')})")
        else:
            logger.warning(f"Biomass model not found at {model_path}")
    return _biomass_model_data


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


def predict_biomass_from_features(feature_dict: dict) -> float:
    """
    Predict biomass using the trained Random Forest model.
    
    Args:
        feature_dict: Dictionary with 13 features:
            {blue, green, red, nir, swir1, swir2, ndvi, evi, savi, ndmi, nbr, elevation, slope}
    
    Returns:
        Predicted biomass in tonnes/ha
    """
    model_data = _load_biomass_model()
    
    if model_data is None:
        logger.error("Biomass model not loaded, using fallback formula")
        # Fallback formula
        ndvi = feature_dict.get('ndvi', 0.5)
        evi = feature_dict.get('evi', 0.3)
        biomass = ndvi * 300 + evi * 50
        return round(float(np.clip(biomass, 5, 400)), 2)
    
    try:
        # Get feature order from model
        feature_cols = model_data['feature_cols']
        
        # Build feature array in correct order
        X = np.array([[feature_dict[col] for col in feature_cols]])
        
        # Apply scaler
        scaler = model_data['scaler']
        X_scaled = scaler.transform(X)
        
        # Predict
        model = model_data['model']
        prediction = model.predict(X_scaled)[0]
        
        # Clip to reasonable range
        biomass = float(np.clip(prediction, 1, 500))
        
        logger.info(f"Predicted biomass: {biomass:.2f} tonnes/ha (NDVI={feature_dict['ndvi']:.3f})")
        return round(biomass, 2)
        
    except Exception as e:
        logger.error(f"Error predicting biomass: {e}")
        # Fallback
        ndvi = feature_dict.get('ndvi', 0.5)
        biomass = ndvi * 300
        return round(float(np.clip(biomass, 5, 400)), 2)


def estimate_biomass(
    ndvi: float,
    evi: float,
    elevation: float,
    slope: float,
    precip: float,
    land_use: str,
) -> float:
    """Legacy function for backward compatibility. Use predict_biomass_from_features for real predictions."""
    model_data = _load_biomass_model()
    land_type = LAND_USE_ENCODING.get(land_use, 2)

    if model_data is not None and 'model' in model_data:
        # This is a simplified version, may not match training features
        logger.warning("Using legacy estimate_biomass - consider using predict_biomass_from_features with full features")
        features = np.array([[ndvi, evi, elevation, slope, precip, land_type]])
        # Note: This won't work correctly with the real model which expects 13 features
        # Fallback to formula
        
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

import os
import logging

try:
    import joblib
    import numpy as np
    _ML_AVAILABLE = True
except ImportError:
    _ML_AVAILABLE = False

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
    if not _ML_AVAILABLE:
        return None
    if _biomass_model_data is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "biomass_model_v1.pkl")
        abs_model_path = os.path.abspath(model_path)
        
        logger.info(f"🔍 Attempting to load biomass model...")
        logger.info(f"   Relative path: {model_path}")
        logger.info(f"   Absolute path: {abs_model_path}")
        logger.info(f"   File exists: {os.path.exists(model_path)}")
        
        if os.path.exists(model_path):
            try:
                _biomass_model_data = joblib.load(model_path)
                logger.info(f"✅ Successfully loaded biomass model v1")
                logger.info(f"   Test R²: {_biomass_model_data.get('test_r2', 'N/A')}")
                logger.info(f"   Test RMSE: {_biomass_model_data.get('test_rmse', 'N/A')}")
                logger.info(f"   Features: {len(_biomass_model_data.get('feature_cols', []))}")
                logger.info(f"   Model type: {type(_biomass_model_data.get('model', None)).__name__}")
            except Exception as e:
                logger.error(f"❌ Error loading model file: {type(e).__name__}: {str(e)}")
                logger.error(f"   Full traceback:", exc_info=True)
                _biomass_model_data = None
        else:
            logger.warning(f"❌ Biomass model file not found at {abs_model_path}")
            logger.warning(f"   Current working directory: {os.getcwd()}")
            logger.warning(f"   Directory of this file: {os.path.dirname(__file__)}")
            
            # List what's actually in the models directory
            models_dir = os.path.join(os.path.dirname(__file__), "..", "ml", "models")
            if os.path.exists(models_dir):
                logger.info(f"   Contents of models directory:")
                for item in os.listdir(models_dir):
                    logger.info(f"      - {item}")
            else:
                logger.warning(f"   Models directory does not exist: {models_dir}")
    return _biomass_model_data


def _load_integrity_model():
    global _integrity_model
    if not _ML_AVAILABLE:
        return None
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
    logger.info("=" * 60)
    logger.info("BIOMASS PREDICTION DEBUG TRACE")
    logger.info("=" * 60)
    
    model_data = _load_biomass_model()
    
    if model_data is None:
        logger.error("❌ FALLBACK MODE: Biomass model not loaded!")
        logger.error(f"   Model path checked: {os.path.join(os.path.dirname(__file__), '..', 'ml', 'models', 'biomass_model_v1.pkl')}")
        logger.error("   Using simple NDVI formula instead of trained model")
        # Fallback formula
        ndvi = feature_dict.get('ndvi', 0.5)
        evi = feature_dict.get('evi', 0.3)
        biomass = ndvi * 300 + evi * 50
        logger.warning(f"   Fallback result: {biomass:.2f} tonnes/ha (NDVI={ndvi:.3f}, EVI={evi:.3f})")
        return round(float(max(5.0, min(400.0, biomass))), 2)

    # Model is loaded - verify its contents
    logger.info("✅ Model data loaded successfully!")
    logger.info(f"   Model type: {type(model_data)}")
    logger.info(f"   Model keys: {list(model_data.keys())}")
    
    if 'test_r2' in model_data:
        logger.info(f"   Model R² Score: {model_data['test_r2']:.4f}")
    if 'test_rmse' in model_data:
        logger.info(f"   Model RMSE: {model_data['test_rmse']:.2f}")
    
    try:
        # Get feature order from model
        feature_cols = model_data['feature_cols']
        logger.info(f"   Expected features ({len(feature_cols)}): {feature_cols}")
        logger.info(f"   Provided features ({len(feature_dict)}): {list(feature_dict.keys())}")
        
        # Check if all required features are present
        missing_features = [col for col in feature_cols if col not in feature_dict]
        if missing_features:
            logger.error(f"   ❌ Missing features: {missing_features}")
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Build feature array in correct order
        X = np.array([[feature_dict[col] for col in feature_cols]])
        logger.info(f"   Feature array shape: {X.shape}")
        logger.info(f"   Feature values: {X[0][:5]}... (showing first 5)")
        
        # Apply scaler
        scaler = model_data['scaler']
        X_scaled = scaler.transform(X)
        logger.info(f"   Scaled features: {X_scaled[0][:5]}... (showing first 5)")
        
        # Predict
        model = model_data['model']
        model_type = type(model).__name__
        logger.info(f"   Model type: {model_type}")
        
        prediction = model.predict(X_scaled)[0]
        logger.info(f"   Raw prediction: {prediction:.2f} tonnes/ha")
        
        # Clip to reasonable range
        biomass = float(max(1.0, min(500.0, prediction)))
        logger.info(f"   Final prediction (clipped): {biomass:.2f} tonnes/ha")
        
        logger.info(f"✅ USING TRAINED MODEL: {biomass:.2f} tonnes/ha (NDVI={feature_dict['ndvi']:.3f})")
        logger.info("=" * 60)
        return round(biomass, 2)
        
    except Exception as e:
        logger.error(f"❌ ERROR during model prediction: {type(e).__name__}: {str(e)}")
        logger.error(f"   Full traceback:", exc_info=True)
        logger.error("   Falling back to formula-based estimation")
        # Fallback
        ndvi = feature_dict.get('ndvi', 0.5)
        biomass = ndvi * 300
        result = round(float(max(5.0, min(400.0, biomass))), 2)
        logger.warning(f"   Fallback result: {result:.2f} tonnes/ha")
        logger.info("=" * 60)
        return result


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

    # Fallback formula if model not trained yet
    biomass = ndvi * 300 + evi * 50 + (precip - 800) / 1200 * 40 - slope * 0.5
    return round(float(max(5.0, min(350.0, biomass))), 2)


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

    if model is not None and _ML_AVAILABLE:
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
        return round(float(max(0.0, min(100.0, score))), 1)

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
    return round(float(max(0.0, min(100.0, score))), 1)

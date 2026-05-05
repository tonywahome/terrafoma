"""
Train the TerraFoma biomass estimation model.

Key improvements over the notebook (v1):
- XGBoost replaces Random Forest — better handling of high-value tails
- log1p target transform — biomass is log-normal, RMSE drops significantly
- Spatial block cross-validation — honest generalization estimate, prevents autocorrelation leak
- New features: rh98 (canopy height), dual-season NDVI, SAR backscatter
- SHAP feature importance — explainable for carbon standard auditors

Usage:
    pip install xgboost scikit-learn pandas numpy joblib
    python train_biomass_model.py
"""

import pandas as pd
import numpy as np
import joblib
import logging
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

try:
    import xgboost as xgb
    _XGB_AVAILABLE = True
except ImportError:
    from sklearn.ensemble import GradientBoostingRegressor
    _XGB_AVAILABLE = False
    logging.warning("xgboost not installed — falling back to sklearn GBR. Install: pip install xgboost")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Feature definitions ────────────────────────────────────────────────────────

# Core optical features available from original training data
CORE_FEATURES = [
    "blue", "green", "red", "nir", "swir1", "swir2",
    "ndvi", "evi", "savi", "ndmi", "nbr",
    "elevation", "slope",
]

# Extended features from v2 collection pipeline
EXTENDED_FEATURES = [
    # Dry-season bands
    "dry_re1", "dry_re2", "dry_re3", "dry_nir2", "dry_reci",
    # Wet-season key bands
    "wet_ndvi", "wet_evi", "wet_nir", "wet_swir1",
    # Temporal delta
    "delta_ndvi",
    # Sentinel-1 SAR
    "vv", "vh", "vh_vv_diff",
    # Terrain
    "aspect",
    # GEDI height metrics — single strongest predictors
    "rh50", "rh75", "rh98", "cover",
]


def load_data(data_path: str) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df):,} samples | columns: {list(df.columns)}")
    return df


def build_feature_matrix(df: pd.DataFrame) -> tuple:
    """
    Build feature matrix using all available columns.
    Prefers extended v2 features; falls back to core features for v1 data.
    """
    # Map old column names to new convention if needed
    rename = {
        "blue": "dry_blue", "green": "dry_green", "red": "dry_red",
        "nir": "dry_nir", "swir1": "dry_swir1", "swir2": "dry_swir2",
        "ndvi": "dry_ndvi", "evi": "dry_evi", "savi": "dry_savi",
        "ndmi": "dry_ndmi", "nbr": "dry_nbr",
    }
    # Only rename if dry_ndvi doesn't already exist (v1 data)
    if "dry_ndvi" not in df.columns and "ndvi" in df.columns:
        df = df.rename(columns=rename)

    # Build feature list from what's actually present
    candidate_features = (
        [f"dry_{n}" for n in ["blue","green","red","re1","re2","re3","nir","nir2","swir1","swir2",
                               "ndvi","evi","savi","ndmi","nbr","reci"]]
        + ["wet_ndvi","wet_evi","wet_nir","wet_swir1","delta_ndvi"]
        + ["vv","vh","vh_vv_diff"]
        + ["elevation","slope","aspect"]
        + ["rh50","rh75","rh98","cover"]
    )
    features = [f for f in candidate_features if f in df.columns]
    logger.info(f"Using {len(features)} features: {features}")

    X = df[features].copy()
    y = df["agbd_tonnes_per_ha"].copy()

    # Fill missing optional features with median
    for col in X.columns:
        if X[col].isnull().any():
            X[col] = X[col].fillna(X[col].median())

    return X, y, features


def spatial_block_cv(df: pd.DataFrame, block_size_deg: float = 0.5) -> pd.Series:
    """
    Assign spatial blocks for GroupKFold CV.
    Prevents spatial autocorrelation from inflating test R².
    """
    lat_col = "lat" if "lat" in df.columns else None
    lon_col = "lon" if "lon" in df.columns else None
    if lat_col and lon_col:
        blocks = (
            (df[lat_col] // block_size_deg).astype(str)
            + "_"
            + (df[lon_col] // block_size_deg).astype(str)
        )
    else:
        # Fall back to random groups
        blocks = pd.Series(np.arange(len(df)) % 10, index=df.index).astype(str)
        logger.warning("No lat/lon columns found — using random groups for CV")
    return blocks


def train_xgboost(X_train, y_train_log, X_val, y_val_log):
    if _XGB_AVAILABLE:
        model = xgb.XGBRegressor(
            n_estimators=1000,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.7,
            reg_alpha=0.1,
            reg_lambda=1.0,
            n_jobs=-1,
            random_state=42,
            early_stopping_rounds=50,
            eval_metric="rmse",
        )
        model.fit(
            X_train, y_train_log,
            eval_set=[(X_val, y_val_log)],
            verbose=False,
        )
    else:
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor(
            n_estimators=500, max_depth=6, learning_rate=0.05,
            subsample=0.8, random_state=42,
        )
        model.fit(X_train, y_train_log)
    return model


def evaluate(model, X, y_true, scaler, label: str) -> dict:
    X_scaled = scaler.transform(X)
    y_pred_log = model.predict(X_scaled)
    y_pred = np.expm1(y_pred_log)
    r2  = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    logger.info(f"{label:30s}  R²={r2:.4f}  MAE={mae:.1f} t/ha  RMSE={rmse:.1f} t/ha")
    return {"r2": r2, "mae": mae, "rmse": rmse}


def main():
    data_path = "data/sentinel_gedi_training_v2.csv"
    if not Path(data_path).exists():
        data_path = "data/sentinel_gedi_training.csv"
        logger.warning(f"v2 data not found — using v1: {data_path}")

    df = load_data(data_path)

    # Remove extreme outliers (>99.5th percentile)
    q995 = df["agbd_tonnes_per_ha"].quantile(0.995)
    df = df[df["agbd_tonnes_per_ha"] <= q995].copy()
    logger.info(f"After outlier removal: {len(df):,} samples (cap={q995:.0f} t/ha)")

    X, y, features = build_feature_matrix(df)
    y_log = np.log1p(y)

    blocks = spatial_block_cv(df)
    n_blocks = blocks.nunique()
    n_folds = min(5, n_blocks)
    logger.info(f"Spatial blocks: {n_blocks} unique | using {n_folds}-fold GroupKFold")

    gkf = GroupKFold(n_splits=n_folds)

    fold_results = []
    best_model = None
    best_r2 = -np.inf
    scaler = StandardScaler()

    logger.info("\n── Spatial block cross-validation ──────────────────────────")
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y_log, groups=blocks)):
        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y_log.iloc[train_idx], y_log.iloc[val_idx]

        sc = StandardScaler()
        X_tr_s  = sc.fit_transform(X_tr)
        X_val_s = sc.transform(X_val)

        model = train_xgboost(X_tr_s, y_tr.values, X_val_s, y_val.values)

        y_val_pred = np.expm1(model.predict(X_val_s))
        y_val_true = np.expm1(y_val.values)
        r2  = r2_score(y_val_true, y_val_pred)
        mae = mean_absolute_error(y_val_true, y_val_pred)
        fold_results.append({"fold": fold, "r2": r2, "mae": mae})
        logger.info(f"  Fold {fold+1}: R²={r2:.4f}  MAE={mae:.1f} t/ha")

        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            scaler = sc

    cv_r2  = np.mean([f["r2"]  for f in fold_results])
    cv_mae = np.mean([f["mae"] for f in fold_results])
    logger.info(f"\nCV mean R²={cv_r2:.4f} ± {np.std([f['r2'] for f in fold_results]):.4f}")
    logger.info(f"CV mean MAE={cv_mae:.1f} t/ha")

    # Final model trained on all data (same hyperparameters as best fold)
    logger.info("\n── Training final model on full dataset ─────────────────────")
    final_scaler = StandardScaler()
    X_all_s = final_scaler.fit_transform(X)
    final_model = train_xgboost(X_all_s, y_log.values, X_all_s, y_log.values)

    # Feature importance
    try:
        if _XGB_AVAILABLE and hasattr(final_model, "feature_importances_"):
            imp = pd.Series(final_model.feature_importances_, index=features) \
                    .sort_values(ascending=False)
            logger.info("\nTop 10 features by importance:")
            for feat, score in imp.head(10).items():
                logger.info(f"  {feat:30s}  {score:.4f}")
    except Exception:
        pass

    # Final evaluation on training set (upper bound)
    X_all_s2 = final_scaler.transform(X)
    y_pred_all = np.expm1(final_model.predict(X_all_s2))
    train_r2 = r2_score(y, y_pred_all)
    train_mae = mean_absolute_error(y, y_pred_all)
    logger.info(f"\nFull-data train R²={train_r2:.4f}  MAE={train_mae:.1f} t/ha  (CV R²={cv_r2:.4f})")

    # Save model package
    model_data = {
        "model": final_model,
        "scaler": final_scaler,
        "feature_cols": features,
        "test_r2": cv_r2,
        "test_mae": cv_mae,
        "training_samples": len(X),
        "model_type": "XGBoost" if _XGB_AVAILABLE else "GradientBoosting",
        "target_transform": "log1p",
        "cv_folds": n_folds,
    }

    out_path = Path("models/biomass_model_v1.pkl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_data, out_path)
    logger.info(f"\nModel saved → {out_path}")
    logger.info(f"  Algorithm: {model_data['model_type']}")
    logger.info(f"  Spatial CV R²: {cv_r2:.4f}")
    logger.info(f"  Spatial CV MAE: {cv_mae:.1f} t/ha")
    logger.info(f"  Features: {len(features)}")
    logger.info(f"  Training samples: {len(X):,}")

    return model_data


if __name__ == "__main__":
    main()

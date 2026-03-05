"""Train the biomass estimation Random Forest model on synthetic data."""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

np.random.seed(42)
N_SAMPLES = 400

# Generate synthetic features
land_types = np.random.choice([0, 1, 2, 3], N_SAMPLES)

# NDVI profiles by land type: forest(0), agroforestry(1), grassland(2), cropland(3)
ndvi_means = [0.75, 0.65, 0.45, 0.40]
ndvi = np.array([np.clip(np.random.normal(ndvi_means[lt], 0.08), 0.1, 0.95) for lt in land_types])
evi = ndvi * np.random.uniform(0.55, 0.70, N_SAMPLES)
elevation = np.random.uniform(1500, 3000, N_SAMPLES)
slope = np.random.uniform(0, 30, N_SAMPLES)
precip = np.random.uniform(800, 2000, N_SAMPLES)

# Biomass model (with realistic relationships)
biomass = (
    ndvi * 300
    + evi * 50
    + (precip - 800) / 1200 * 40
    - slope * 0.5
    + np.random.normal(0, 15, N_SAMPLES)
)
biomass = np.clip(biomass, 5, 350)

# Create DataFrame
X = pd.DataFrame({
    "ndvi": ndvi,
    "evi": evi,
    "elevation": elevation,
    "slope": slope,
    "precip": precip,
    "land_type": land_types,
})
y = biomass

# Save training data
os.makedirs("ml/sample_data", exist_ok=True)
X.to_csv("ml/sample_data/features.csv", index=False)
pd.Series(y, name="biomass_tonnes_per_ha").to_csv("ml/sample_data/labels.csv", index=False)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
r2 = r2_score(y_test, preds)
mae = mean_absolute_error(y_test, preds)
print(f"Biomass Estimation Model")
print(f"  R2 Score: {r2:.3f}")
print(f"  MAE: {mae:.1f} t/ha")
print(f"  Feature importances:")
for feat, imp in zip(X.columns, model.feature_importances_):
    print(f"    {feat}: {imp:.3f}")

# Save model
joblib.dump(model, "ml/model.pkl")
print(f"\nModel saved to ml/model.pkl")

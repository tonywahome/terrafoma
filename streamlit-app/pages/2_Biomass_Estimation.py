import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

st.set_page_config(page_title="Biomass Estimation", page_icon="🌳", layout="wide")
st.title("🌳 Biomass Estimation Model")
st.markdown("Interactive demo of the Random Forest biomass estimation model.")

# Try to load the trained model
model_path = os.path.join(os.path.dirname(__file__), "..", "..", "backend", "ml", "model.pkl")
model = None
if os.path.exists(model_path):
    model = joblib.load(model_path)

# Interactive inputs
st.sidebar.header("Input Features")
ndvi = st.sidebar.slider("NDVI", 0.1, 0.95, 0.65, 0.01)
evi = st.sidebar.slider("EVI", 0.05, 0.7, 0.40, 0.01)
elevation = st.sidebar.slider("Elevation (m)", 1500, 3000, 2000, 50)
slope = st.sidebar.slider("Slope (degrees)", 0, 30, 10, 1)
precip = st.sidebar.slider("Annual Precipitation (mm)", 800, 2000, 1200, 50)
land_type = st.sidebar.selectbox("Land Type", ["Forest", "Agroforestry", "Grassland", "Cropland"])
land_type_encoded = {"Forest": 0, "Agroforestry": 1, "Grassland": 2, "Cropland": 3}[land_type]

# Prediction
col1, col2, col3 = st.columns(3)

if model:
    features = np.array([[ndvi, evi, elevation, slope, precip, land_type_encoded]])
    biomass = model.predict(features)[0]
    biomass = np.clip(biomass, 5, 350)
else:
    biomass = ndvi * 300 + evi * 50 + (precip - 800) / 1200 * 40 - slope * 0.5
    biomass = np.clip(biomass, 5, 350)

tco2e_per_ha = biomass * 0.47 * 3.667

with col1:
    st.metric("Estimated Biomass", f"{biomass:.1f} t/ha")
with col2:
    st.metric("Carbon Stock", f"{tco2e_per_ha:.1f} tCO2e/ha")
with col3:
    st.metric("Model Type", "Random Forest" if model else "Fallback Formula")

st.markdown("---")

# Feature importance
if model and hasattr(model, "feature_importances_"):
    st.subheader("Feature Importances")
    feat_names = ["NDVI", "EVI", "Elevation", "Slope", "Precipitation", "Land Type"]
    importances = model.feature_importances_

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#16a34a" if i == np.argmax(importances) else "#86efac" for i in range(len(importances))]
    ax.barh(feat_names, importances, color=colors)
    ax.set_xlabel("Importance")
    ax.set_title("Random Forest Feature Importances")
    st.pyplot(fig)

# Conversion formula
st.markdown("---")
st.subheader("Conversion Formula")
st.latex(r"tCO_2e = \text{Biomass} \times 0.47 \times 3.667 \times \text{Area (ha)}")
st.markdown("""
- **0.47**: Carbon fraction of dry biomass (IPCC default)
- **3.667**: Molecular weight ratio of CO2 to C (44/12)
""")

# Scatter: predicted vs inputs
st.markdown("---")
st.subheader("Model Response Curves")

fig2, axes = plt.subplots(1, 3, figsize=(15, 4))
if model:
    # NDVI sweep
    ndvi_range = np.linspace(0.1, 0.95, 50)
    biomass_ndvi = [model.predict([[n, evi, elevation, slope, precip, land_type_encoded]])[0] for n in ndvi_range]
    axes[0].plot(ndvi_range, biomass_ndvi, color="#16a34a", linewidth=2)
    axes[0].axvline(ndvi, color="red", linestyle="--", alpha=0.5)
    axes[0].set_xlabel("NDVI")
    axes[0].set_ylabel("Biomass (t/ha)")
    axes[0].set_title("NDVI vs Biomass")

    # Precipitation sweep
    precip_range = np.linspace(800, 2000, 50)
    biomass_precip = [model.predict([[ndvi, evi, elevation, slope, p, land_type_encoded]])[0] for p in precip_range]
    axes[1].plot(precip_range, biomass_precip, color="#0891b2", linewidth=2)
    axes[1].axvline(precip, color="red", linestyle="--", alpha=0.5)
    axes[1].set_xlabel("Precipitation (mm)")
    axes[1].set_ylabel("Biomass (t/ha)")
    axes[1].set_title("Precipitation vs Biomass")

    # Elevation sweep
    elev_range = np.linspace(1500, 3000, 50)
    biomass_elev = [model.predict([[ndvi, evi, e, slope, precip, land_type_encoded]])[0] for e in elev_range]
    axes[2].plot(elev_range, biomass_elev, color="#d97706", linewidth=2)
    axes[2].axvline(elevation, color="red", linestyle="--", alpha=0.5)
    axes[2].set_xlabel("Elevation (m)")
    axes[2].set_ylabel("Biomass (t/ha)")
    axes[2].set_title("Elevation vs Biomass")

plt.tight_layout()
st.pyplot(fig2)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Satellite Analysis", page_icon="🛰️", layout="wide")
st.title("🛰️ Satellite Analysis")
st.markdown("Simulated Sentinel-2 spectral band analysis for vegetation monitoring.")

# Land use selector
land_use = st.selectbox("Select Land Use Type", ["forest", "agroforestry", "grassland", "cropland"])

# Band profiles
PROFILES = {
    "forest": {"B2": 0.03, "B3": 0.05, "B4": 0.03, "B8": 0.40, "B11": 0.15, "B12": 0.08},
    "agroforestry": {"B2": 0.04, "B3": 0.06, "B4": 0.05, "B8": 0.35, "B11": 0.18, "B12": 0.10},
    "grassland": {"B2": 0.05, "B3": 0.08, "B4": 0.06, "B8": 0.28, "B11": 0.22, "B12": 0.15},
    "cropland": {"B2": 0.06, "B3": 0.09, "B4": 0.07, "B8": 0.25, "B11": 0.20, "B12": 0.14},
}

bands = PROFILES[land_use]

# Band comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spectral Band Reflectance")
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#2563eb", "#16a34a", "#dc2626", "#7c3aed", "#d97706", "#0891b2"]
    ax.bar(bands.keys(), bands.values(), color=colors)
    ax.set_ylabel("Reflectance")
    ax.set_xlabel("Sentinel-2 Band")
    ax.set_title(f"Spectral Profile: {land_use.capitalize()}")
    st.pyplot(fig)

with col2:
    # NDVI calculation
    ndvi = (bands["B8"] - bands["B4"]) / (bands["B8"] + bands["B4"])
    evi = 2.5 * (bands["B8"] - bands["B4"]) / (bands["B8"] + 6 * bands["B4"] - 7.5 * bands["B2"] + 1)

    st.subheader("Vegetation Indices")
    st.metric("NDVI", f"{ndvi:.4f}", help="Normalized Difference Vegetation Index")
    st.metric("EVI", f"{evi:.4f}", help="Enhanced Vegetation Index")
    st.info(f"**NDVI** ranges from -1 to 1. Values > 0.6 indicate dense vegetation. "
            f"**{land_use.capitalize()}** shows NDVI = {ndvi:.3f}")

# NDVI heatmap simulation
st.markdown("---")
st.subheader("Simulated NDVI Heatmap (10x10 pixel grid)")

np.random.seed(42 + hash(land_use) % 100)
grid_size = 10
ndvi_grid = np.random.normal(ndvi, 0.08, (grid_size, grid_size))
ndvi_grid = np.clip(ndvi_grid, -0.1, 1.0)

fig2, ax2 = plt.subplots(figsize=(8, 6))
im = ax2.imshow(ndvi_grid, cmap="RdYlGn", vmin=0, vmax=1, interpolation="bilinear")
ax2.set_title(f"NDVI Heatmap - {land_use.capitalize()}")
plt.colorbar(im, ax=ax2, label="NDVI")
ax2.set_xlabel("Pixel X")
ax2.set_ylabel("Pixel Y")
st.pyplot(fig2)

# Temporal NDVI slider
st.markdown("---")
st.subheader("Temporal NDVI Simulation")
season = st.slider("Season (months)", 1, 12, 6)

seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * (season - 3) / 12)
seasonal_ndvi = ndvi * seasonal_factor
st.metric("Seasonal NDVI", f"{seasonal_ndvi:.4f}",
          delta=f"{(seasonal_ndvi - ndvi):.4f} from baseline")

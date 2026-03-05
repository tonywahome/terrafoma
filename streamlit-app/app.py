import streamlit as st

st.set_page_config(
    page_title="TerraFoma - AI Analysis",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 TerraFoma AI Analysis Suite")
st.markdown("---")

st.markdown("""
## Welcome to the TerraFoma Analysis Tool

This suite provides technical insights into our AI-powered carbon credit verification system.

### Pages

- **Satellite Analysis** - Explore Sentinel-2 spectral bands and vegetation indices (NDVI, EVI)
- **Biomass Estimation** - Interactive demo of our Random Forest biomass model
- **Risk Assessment** - Visualize environmental risk factors for carbon projects

### Architecture

```
Satellite Data (Sentinel-2) → Spectral Analysis (NDVI/EVI)
    ↓
Biomass Estimation (Random Forest) → tCO2e Calculation
    ↓
Risk Assessment (Weather + Fire + Deforestation) → Integrity Score
    ↓
Credit Pricing → Marketplace
```

Use the sidebar to navigate between analysis pages.
""")

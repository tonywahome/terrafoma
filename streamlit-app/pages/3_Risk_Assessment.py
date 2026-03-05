import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Risk Assessment", page_icon="⚠️", layout="wide")
st.title("⚠️ Risk Assessment")
st.markdown("Environmental and permanence risk scoring for carbon projects.")

WEATHER = {
    "Nyeri": {"avg_temp": 18, "precip_mm": 1200, "drought_index": 0.2, "fire_events_5yr": 1},
    "Laikipia": {"avg_temp": 22, "precip_mm": 700, "drought_index": 0.6, "fire_events_5yr": 4},
    "Murang'a": {"avg_temp": 19, "precip_mm": 1500, "drought_index": 0.15, "fire_events_5yr": 0},
    "Nyandarua": {"avg_temp": 14, "precip_mm": 1100, "drought_index": 0.25, "fire_events_5yr": 2},
}

region = st.selectbox("Select Region", list(WEATHER.keys()))
land_use = st.selectbox("Land Use", ["forest", "agroforestry", "grassland", "cropland"])

weather = WEATHER[region]

# Risk calculations
drought_risk = weather["drought_index"]
wildfire_risk = min(weather["fire_events_5yr"] / 10, 1.0)
deforestation_risk = {"forest": 0.3, "agroforestry": 0.15, "grassland": 0.05, "cropland": 0.02}[land_use]
political_risk = 0.1

composite = (
    drought_risk * 0.3 + wildfire_risk * 0.3 +
    deforestation_risk * 0.25 + political_risk * 0.15
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Dimensions")

    # Radar chart
    categories = ["Drought", "Wildfire", "Deforestation", "Political"]
    values = [drought_risk, wildfire_risk, deforestation_risk, political_risk]
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(220, 38, 38, 0.2)",
        line=dict(color="rgb(220, 38, 38)", width=2),
        name="Risk"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Risk Breakdown")

    for name, val in zip(categories, values):
        color = "green" if val < 0.3 else "orange" if val < 0.6 else "red"
        st.progress(val, text=f"{name}: {val:.0%}")

    st.markdown("---")
    risk_color = "🟢" if composite < 0.3 else "🟡" if composite < 0.5 else "🔴"
    st.metric("Composite Risk Score", f"{composite:.1%}", help="Weighted average of all risk dimensions")
    st.markdown(f"{risk_color} Risk Level: **{'Low' if composite < 0.3 else 'Medium' if composite < 0.5 else 'High'}**")

# Pricing impact
st.markdown("---")
st.subheader("Impact on Credit Pricing")

base_price = 15.00
adjusted_price = base_price * (1 - composite * 0.3)

col3, col4, col5 = st.columns(3)
with col3:
    st.metric("Base Price", f"${base_price:.2f}/t")
with col4:
    st.metric("Risk Discount", f"-{composite * 30:.1f}%")
with col5:
    st.metric("Adjusted Price", f"${adjusted_price:.2f}/t",
              delta=f"${adjusted_price - base_price:.2f}")

st.info(f"**Formula:** `adjusted_price = ${base_price} x (1 - {composite:.3f} x 0.3) = ${adjusted_price:.2f}`")

# Weather data
st.markdown("---")
st.subheader(f"Weather Profile: {region}")
wcol1, wcol2, wcol3, wcol4 = st.columns(4)
wcol1.metric("Avg Temp", f"{weather['avg_temp']}°C")
wcol2.metric("Precipitation", f"{weather['precip_mm']} mm/yr")
wcol3.metric("Drought Index", f"{weather['drought_index']:.2f}")
wcol4.metric("Fire Events (5yr)", str(weather["fire_events_5yr"]))

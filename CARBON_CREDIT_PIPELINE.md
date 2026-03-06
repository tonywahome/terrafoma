# Terrafoma Carbon Credit Generation Pipeline

**Complete Technical Documentation: From Area Selection to Carbon Credit Pricing**

---

## Table of Contents

1. [Overview](#overview)
2. [Area Selection & Geometry Processing](#1-area-selection--geometry-processing)
3. [Satellite Feature Extraction](#2-satellite-feature-extraction)
4. [Biomass Prediction Model](#3-biomass-prediction-model)
5. [Carbon Calculation Engine](#4-carbon-calculation-engine)
6. [Risk Assessment](#5-risk-assessment)
7. [Integrity Score Calculation](#6-integrity-score-calculation)
8. [Price Determination](#7-price-determination)
9. [Credit Creation & Storage](#8-credit-creation--storage)
10. [Variable Definitions Reference](#9-variable-definitions-reference)

---

## Overview

The Terrafoma platform converts land conservation efforts into verifiable carbon credits through a multi-stage pipeline that combines:
- **Satellite remote sensing** (Sentinel-2 imagery via Google Earth Engine)
- **Machine learning** (Random Forest biomass prediction)
- **Carbon science** (IPCC carbon accounting methods)
- **Risk modeling** (Environmental and socio-political factors)
- **Market-based pricing** (Voluntary carbon market standards)

---

## 1. Area Selection & Geometry Processing

### User Action
User draws a polygon on an interactive Mapbox map representing their land plot.

### Backend Processing

**File:** `backend/routers/scan.py` (Lines 18-70)

```python
# Step 1.1: Geometry received as GeoJSON
request.geometry = {
    "type": "Polygon",
    "coordinates": [[[lon1, lat1], [lon2, lat2], ...]]
}

# Step 1.2: Extract geographic location
location = get_location_from_geometry(request.geometry)
# Uses Nominatim reverse geocoding API
# Output: "Laikipia East, Kenya"

# Step 1.3: Create or retrieve land plot record
plot = {
    "id": UUID,
    "owner_id": UUID,
    "name": f"Plot at {location}",
    "geometry": GeoJSON,
    "area_hectares": calculated_area,  # From polygon bounds
    "region": location,
    "land_use": "forest"  # User-specified or default
}
```

**Key Variables:**
- `geometry`: GeoJSON object (Point, Polygon, or MultiPolygon)
- `area_hectares`: Land area in hectares (1 hectare = 10,000 m²)
- `land_use`: Classification (forest, agroforestry, grassland, cropland, wetland)
- `region`: Geographic location name from reverse geocoding

---

## 2. Satellite Feature Extraction

### Process: Real-Time Sentinel-2 Data Collection

**File:** `backend/services/gee_feature_extractor.py`

### 2.1 Satellite Data Source
- **Sensor:** Sentinel-2 MultiSpectral Instrument (MSI)
- **Resolution:** 10m for visible/NIR, 20m for SWIR bands
- **Time Period:** 2023-01-01 to 2024-12-31 (24 months)
- **Cloud Filtering:** Images with >30% cloud cover rejected

### 2.2 Spectral Bands Extracted

```python
# Raw Sentinel-2 Bands (Mean values across time period)
B2 (Blue):    0.05   # 490 nm - Atmospheric scattering, water
B3 (Green):   0.08   # 560 nm - Peak vegetation reflectance
B4 (Red):     0.06   # 665 nm - Chlorophyll absorption
B8 (NIR):     0.45   # 842 nm - Plant cell structure
B11 (SWIR1):  0.25   # 1610 nm - Moisture content
B12 (SWIR2):  0.15   # 2190 nm - Geology, soil moisture
```

### 2.3 Calculated Vegetation Indices

These indices are computed from band combinations to highlight vegetation characteristics:

#### NDVI - Normalized Difference Vegetation Index
```python
NDVI = (NIR - Red) / (NIR + Red)
# Range: -1 to +1
# Typical values:
#   0.7-1.0 = Dense forest
#   0.4-0.7 = Moderate vegetation
#   0.2-0.4 = Sparse vegetation
#   < 0.2   = Bare soil/water
```

#### EVI - Enhanced Vegetation Index
```python
EVI = 2.5 × ((NIR - Red) / (NIR + 6×Red - 7.5×Blue + 1))
# More sensitive to high biomass areas than NDVI
# Less affected by atmospheric conditions
```

#### SAVI - Soil-Adjusted Vegetation Index
```python
SAVI = ((NIR - Red) / (NIR + Red + 0.5)) × 1.5
# Minimizes soil brightness influences
# Better for sparse vegetation
```

#### NDMI - Normalized Difference Moisture Index
```python
NDMI = (NIR - SWIR1) / (NIR + SWIR1)
# Indicates vegetation water content
# Higher values = more moisture
```

#### NBR - Normalized Burn Ratio
```python
NBR = (NIR - SWIR2) / (NIR + SWIR2)
# Fire severity assessment
# Healthy vegetation: 0.4-0.6
```

### 2.4 Topographic Features

**Source:** SRTM Digital Elevation Model (30m resolution)

```python
elevation:  1600-2800 meters (Kenya highlands typical range)
slope:      2-18 degrees (terrain steepness)
```

### 2.5 Complete Feature Vector

After extraction, we have **13 features** for biomass prediction:

```python
features = {
    'blue':      0.05,    # B2 reflectance
    'green':     0.08,    # B3 reflectance
    'red':       0.06,    # B4 reflectance
    'nir':       0.45,    # B8 reflectance
    'swir1':     0.25,    # B11 reflectance
    'swir2':     0.15,    # B12 reflectance
    'ndvi':      0.65,    # Vegetation density
    'evi':       0.52,    # Enhanced vegetation
    'savi':      0.58,    # Soil-adjusted vegetation
    'ndmi':      0.35,    # Moisture index
    'nbr':       0.40,    # Burn ratio
    'elevation': 1200.0,  # Height above sea level (m)
    'slope':     5.0      # Terrain angle (degrees)
}
```

**File:** Returns from `extract_sentinel_features()` → `scan.py` Line 78

---

## 3. Biomass Prediction Model

### Model Architecture: Random Forest Regressor

**File:** `backend/services/biomass_estimator.py`

### 3.1 Model Training Source
- **Training Data:** GEDI (Global Ecosystem Dynamics Investigation) LiDAR biomass measurements
- **Training Samples:** 10,000+ observations from Congo Basin forests
- **Model Type:** Scikit-learn RandomForestRegressor
- **Performance:** R² = 0.532, RMSE = 31.98 tonnes/ha
- **Model File:** `backend/ml/models/biomass_model_v1.pkl`

### 3.2 Prediction Pipeline

```python
def predict_biomass_from_features(feature_dict: dict) -> float:
    # Step 3.2.1: Load trained model
    model_data = joblib.load('biomass_model_v1.pkl')
    model = model_data['model']            # RandomForestRegressor
    scaler = model_data['scaler']          # StandardScaler
    feature_cols = model_data['feature_cols']  # Feature order
    
    # Step 3.2.2: Arrange features in training order
    X = np.array([[feature_dict[col] for col in feature_cols]])
    # X shape: (1, 13)
    
    # Step 3.2.3: Normalize features (zero mean, unit variance)
    X_scaled = scaler.transform(X)
    
    # Step 3.2.4: Predict biomass using Random Forest ensemble
    biomass = model.predict(X_scaled)[0]
    # Output: tonnes/hectare (dry aboveground biomass)
    
    # Step 3.2.5: Clip to realistic range
    biomass = np.clip(biomass, 1, 500)  # tonnes/ha
    
    return biomass  # e.g., 85.98 tonnes/ha
```

### 3.3 Biomass Interpretation

**What is Biomass?**
- **Definition:** Total dry weight of living plant matter above ground
- **Units:** Tonnes per hectare (t/ha)
- **Components:** Trees, shrubs, understory vegetation, deadwood

**Typical Ranges:**
- Dense tropical forest: 150-400 t/ha
- Moderate forest: 50-150 t/ha
- Agroforestry: 20-80 t/ha
- Grassland: 5-20 t/ha

---

## 4. Carbon Calculation Engine

### 4.1 Biomass to Carbon Conversion

**File:** `backend/services/biomass_estimator.py` (Line 46-49)

```python
def biomass_to_tco2e(biomass_tonnes_per_ha: float, area_hectares: float) -> float:
    # Step 4.1.1: Calculate carbon content
    carbon_fraction = 0.47  # IPCC default: 47% of biomass is carbon
    carbon_tonnes = biomass_tonnes_per_ha × carbon_fraction
    
    # Step 4.1.2: Convert carbon to CO₂ equivalent
    co2_ratio = 3.667  # Molecular weight ratio: CO₂(44) / C(12)
    tco2e_per_ha = carbon_tonnes × co2_ratio
    
    # Step 4.1.3: Scale to total area
    total_tco2e = tco2e_per_ha × area_hectares
    
    return total_tco2e
```

### 4.2 Example Calculation

```
Input:
  - Biomass: 85.98 tonnes/ha
  - Area: 10 hectares

Calculation:
  - Carbon = 85.98 × 0.47 = 40.41 tonnes C/ha
  - CO₂e = 40.41 × 3.667 = 148.14 tCO₂e/ha
  - Total = 148.14 × 10 = 1,481.4 tCO₂e

Output: 1,481.4 tonnes of CO₂ equivalent sequestered
```

### 4.3 Carbon Density Metric

```python
carbon_density = total_tco2e / area_hectares
# Output: tCO₂e per hectare (intensity metric)
```

**Purpose:** Standardized comparison across different plot sizes

---

## 5. Risk Assessment

### 5.1 Risk Factors Analyzed

**File:** `backend/services/risk_scorer.py`

The platform assesses four categories of risk to carbon permanence:

#### 5.1.1 Drought Risk (30% weight)
```python
drought_index = weather_data['drought_index']  # 0-1 scale
# Based on:
#   - Annual precipitation (mm)
#   - Historical drought frequency
#   - Climate projections
```

**Regional Examples:**
- Laikipia: 0.6 (700mm precipitation, semi-arid)
- Nyeri: 0.2 (1200mm precipitation, well-watered)

#### 5.1.2 Wildfire Risk (30% weight)
```python
wildfire_risk = fire_events_5yr / 10  # Capped at 1.0
# Based on:
#   - Historical fire incidents (5-year lookback)
#   - Vegetation flammability
#   - Fire season intensity
```

**Regional Examples:**
- Laikipia: 0.4 (4 fire events in 5 years)
- Murang'a: 0.0 (No fire events recorded)

#### 5.1.3 Deforestation Risk (25% weight)
```python
deforestation_risk = LAND_USE_RISK[land_use]
```

**Risk by Land Use:**
- Forest: 0.30 (High logging pressure)
- Agroforestry: 0.15 (Moderate conversion risk)
- Grassland: 0.05 (Low threat)
- Wetland: 0.10 (Protected but vulnerable)

#### 5.1.4 Political Risk (15% weight)
```python
political_risk = 0.10  # Regional stability factor
# Considers:
#   - Land tenure security
#   - Policy stability
#   - Governance effectiveness
```

### 5.2 Composite Risk Score

```python
def calculate_risk_score(weather_data, land_use):
    composite_risk = (
        drought_risk      × 0.30 +
        wildfire_risk     × 0.30 +
        deforestation_risk × 0.25 +
        political_risk    × 0.15
    )
    # Range: 0-1 (0 = no risk, 1 = extreme risk)
    return composite_risk
```

**Example:**
```
Laikipia Forest Plot:
  - Drought: 0.6 × 0.30 = 0.18
  - Wildfire: 0.4 × 0.30 = 0.12
  - Deforestation: 0.3 × 0.25 = 0.075
  - Political: 0.1 × 0.15 = 0.015
  
  Composite Risk = 0.39 (Medium-High)
```

---

## 6. Integrity Score Calculation

### Purpose
Quality score (0-100) indicating the reliability and verifiability of carbon estimates.

**File:** `backend/services/biomass_estimator.py` (Line 130-180)

### 6.1 Integrity Components

#### Data Quality (30 points)
```python
data_quality = (
    min(ndvi_mean / 0.8, 1.0) × 15 +        # Vegetation vigor
    max(0, 1 - ndvi_std / 0.2) × 5 +        # Consistency
    max(0, 1 - cloud_cover_pct / 100) × 5 + # Image clarity
    max(0, 1 - scan_resolution_m / 60) × 5   # Spatial detail
)
```

#### Model Confidence (20 points)
```python
model_confidence = biomass_model_r2 × 20
# R² = 0.532 → 10.6 points
```

#### Temporal Stability (20 points)
```python
temporal = (
    max(0, 1 - abs(temporal_ndvi_change) / 0.3) × 10 +  # Stable vegetation
    min(years_under_conservation / 10, 1.0) × 10        # Long-term management
)
```

#### Risk Adjustment (15 points)
```python
risk_adjustment = (
    (1 - drought_risk) × 5 +
    (1 - wildfire_risk) × 5 +
    min(deforestation_proximity_km / 30, 1.0) × 5
)
```

#### Additionality (15 points)
```python
additionality = additionality_score × 15
# Does this project prevent emissions that would otherwise occur?
# Score based on baseline scenario analysis
```

### 6.2 Final Integrity Score

```python
integrity_score = (
    data_quality +
    model_confidence +
    temporal_stability +
    risk_adjustment +
    additionality
)
# Range: 0-100 (higher = more reliable carbon claim)
```

**Interpretation:**
- **90-100:** Premium quality, third-party verified
- **75-89:** High quality, robust monitoring
- **60-74:** Standard quality, adequate verification
- **<60:** Basic quality, additional verification needed

---

## 7. Price Determination

### 7.1 Pricing Algorithm

**File:** `backend/services/carbon_calculator.py` (Line 40-75)

```python
def calculate_credit_price(integrity_score, risk_score):
    # Step 7.1.1: Determine base tier
    if integrity_score >= 90 and risk_score < 0.15:
        base_price = 35.00  # Premium tier
    elif integrity_score >= 75 and risk_score < 0.30:
        base_price = 22.00  # High quality tier
    elif integrity_score >= 60 and risk_score < 0.45:
        base_price = 18.00  # Standard tier
    else:
        base_price = 12.00  # Basic tier
    
    # Step 7.1.2: Fine-tune adjustments
    integrity_bonus = (integrity_score - 50) / 100 × 8  # ±$4
    risk_penalty = risk_score × 10                      # -$0 to -$10
    
    # Step 7.1.3: Calculate final price
    price = base_price + integrity_bonus - risk_penalty
    price = max(price, 12.00)  # Floor at minimum viable price
    
    return round(price, 2)  # USD per tonne CO₂e
```

### 7.2 Pricing Examples

```
Example 1: Premium Forest Credit
  - Integrity: 92
  - Risk: 0.12
  
  Base: $35.00 (premium tier)
  Bonus: (92-50)/100 × 8 = +$3.36
  Penalty: 0.12 × 10 = -$1.20
  Final: $37.16/tonne

Example 2: Standard Grassland Credit
  - Integrity: 68
  - Risk: 0.38
  
  Base: $18.00 (standard tier)
  Bonus: (68-50)/100 × 8 = +$1.44
  Penalty: 0.38 × 10 = -$3.80
  Final: $15.64/tonne

Example 3: Basic Credit
  - Integrity: 52
  - Risk: 0.55
  
  Base: $12.00 (basic tier)
  Bonus: (52-50)/100 × 8 = +$0.16
  Penalty: 0.55 × 10 = -$5.50
  Calculation: $12.00 + $0.16 - $5.50 = $6.66
  Final: $12.00 (floor protection)
```

### 7.3 Market Context

**Voluntary Carbon Market Rates (2024-2026):**
- Nature-based solutions: $10-$50/tonne
- Forestry REDD+: $8-$25/tonne
- Enhanced rock weathering: $60-$200/tonne
- Direct air capture: $400-$1000/tonne

Terrafoma prices align with **forestry conservation projects** in developing markets.

### 7.4 Community Benefit Distribution

```python
credit_value = quantity_tco2e × price_per_tonne

Distribution:
  - Community Direct: 60% ($)
  - Conservation Fund: 25% (ongoing protection)
  - Platform/Verification: 15% (operations)
```

**Example:** 100 tCO₂e credit at $22/tonne = $2,200 total
- Community receives: $1,320
- Conservation fund: $550
- Platform fee: $330

---

## 8. Credit Creation & Storage

### 8.1 Scan Result Record

**Database:** Supabase PostgreSQL  
**Table:** `scan_results`

```python
scan_record = {
    "id": UUID,
    "plot_id": UUID,
    "mean_ndvi": 0.65,
    "mean_evi": 0.52,
    "estimated_biomass": 85.98,      # tonnes/ha
    "estimated_tco2e": 1481.4,       # total tCO₂e
    "carbon_density": 148.14,        # tCO₂e/ha
    "integrity_score": 78.5,
    "model_version": "biomass_model_v1",
    "raw_bands": {
        "B2": 0.05, "B3": 0.08, "B4": 0.06,
        "B8": 0.45, "B11": 0.25, "B12": 0.15,
        "NDVI": 0.65, "EVI": 0.52,
        "elevation": 1200, "slope": 5.0,
        "n_images": 48  # Number of Sentinel-2 scenes used
    }
}
```

### 8.2 Carbon Credit Record

**Table:** `carbon_credits`

```python
credit_record = {
    "id": UUID,
    "scan_id": UUID,                 # Links to scan_results
    "plot_id": UUID,                 # Links to land_plots
    "owner_id": UUID,                # Links to users
    "vintage_year": 2026,            # Year of measurement
    "quantity_tco2e": 1481.4,        # Amount of carbon
    "price_per_tonne": 25.30,        # USD per tonne
    "status": "listed",              # listed/sold/retired/cancelled
    "integrity_score": 78.5,         # Quality score
    "risk_score": 39.0,              # Risk percentage (0-100)
    "created_at": "2026-03-06T14:00:00Z"
}
```

### 8.3 Credit Lifecycle States

```
listed → sold → retired
           ↓
       cancelled (if invalid)
```

- **listed:** Available for purchase in marketplace
- **sold:** Purchased but not yet retired
- **retired:** Permanently applied to offset emissions (cannot be resold)
- **cancelled:** Credit invalidated due to verification issues

---

## 9. Variable Definitions Reference

### Spectral Bands
| Variable | Description | Units | Typical Range |
|----------|-------------|-------|---------------|
| `blue` (B2) | Blue band reflectance | Ratio | 0.02-0.10 |
| `green` (B3) | Green band reflectance | Ratio | 0.04-0.15 |
| `red` (B4) | Red band reflectance | Ratio | 0.02-0.12 |
| `nir` (B8) | Near-infrared reflectance | Ratio | 0.20-0.60 |
| `swir1` (B11) | Shortwave infrared 1 | Ratio | 0.10-0.35 |
| `swir2` (B12) | Shortwave infrared 2 | Ratio | 0.05-0.25 |

### Vegetation Indices
| Variable | Description | Units | Interpretation |
|----------|-------------|-------|----------------|
| `ndvi` | Normalized Difference Vegetation Index | -1 to +1 | >0.6 = Dense vegetation |
| `evi` | Enhanced Vegetation Index | -1 to +1 | >0.4 = Healthy forest |
| `savi` | Soil-Adjusted Vegetation Index | -1 to +1 | Better for sparse areas |
| `ndmi` | Normalized Difference Moisture Index | -1 to +1 | >0.3 = Good moisture |
| `nbr` | Normalized Burn Ratio | -1 to +1 | >0.4 = No fire damage |

### Topographic Variables
| Variable | Description | Units | Source |
|----------|-------------|-------|--------|
| `elevation` | Height above sea level | meters | SRTM DEM |
| `slope` | Terrain steepness | degrees | Derived from DEM |

### Biomass & Carbon
| Variable | Description | Units | Conversion |
|----------|-------------|-------|-----------|
| `biomass` | Aboveground dry biomass | tonnes/ha | From ML model |
| `carbon_tonnes` | Carbon content | tonnes C/ha | biomass × 0.47 |
| `tco2e` | CO₂ equivalent | tonnes CO₂e | carbon × 3.667 |
| `carbon_density` | Carbon per area | tCO₂e/ha | tco2e / area |

### Quality Metrics
| Variable | Description | Units | Range |
|----------|-------------|-------|-------|
| `integrity_score` | Verification quality | points | 0-100 |
| `risk_score` | Permanence risk | ratio | 0-1 |
| `composite_risk` | Overall risk | ratio | 0-1 |

### Risk Components
| Variable | Description | Units | Weight |
|----------|-------------|-------|--------|
| `drought_risk` | Water stress probability | ratio | 30% |
| `wildfire_risk` | Fire probability | ratio | 30% |
| `deforestation_risk` | Clearing probability | ratio | 25% |
| `political_risk` | Governance stability | ratio | 15% |

### Pricing
| Variable | Description | Units | Range |
|----------|-------------|-------|-------|
| `price_per_tonne` | Carbon credit price | USD/tCO₂e | $12-$40 |
| `credit_value` | Total credit value | USD | quantity × price |

---

## Complete Pipeline Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER SELECTS AREA ON MAP                                    │
│    ├─ Draw polygon (GeoJSON)                                   │
│    ├─ Specify land use (forest/agroforestry/grassland)         │
│    └─ Submit scan request                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. EXTRACT SATELLITE FEATURES (Google Earth Engine)            │
│    ├─ Query Sentinel-2: 2023-2024 (24 months)                  │
│    ├─ Filter clouds (<30%)                                     │
│    ├─ Calculate mean reflectance: B2,B3,B4,B8,B11,B12          │
│    ├─ Compute indices: NDVI, EVI, SAVI, NDMI, NBR              │
│    └─ Extract topography: elevation, slope (SRTM)              │
│    → Output: 13-feature vector                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. PREDICT BIOMASS (Random Forest ML Model)                    │
│    ├─ Load model: biomass_model_v1.pkl (R²=0.532)              │
│    ├─ Normalize features (StandardScaler)                      │
│    ├─ Predict: RandomForestRegressor.predict()                 │
│    └─ Output: Biomass in tonnes/ha                             │
│    → Example: 85.98 tonnes/ha                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. CONVERT TO CARBON (IPCC Method)                             │
│    ├─ Carbon = Biomass × 0.47 (carbon fraction)                │
│    ├─ CO₂e = Carbon × 3.667 (molecular weight ratio)           │
│    └─ Total CO₂e = CO₂e/ha × area_hectares                     │
│    → Example: 148.14 tCO₂e/ha × 10ha = 1,481.4 tCO₂e           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. ASSESS RISK (Environmental + Socio-political)               │
│    ├─ Drought risk (precipitation, climate) → 30% weight       │
│    ├─ Wildfire risk (historical fires) → 30% weight            │
│    ├─ Deforestation risk (land use pressure) → 25% weight      │
│    ├─ Political risk (governance) → 15% weight                 │
│    └─ Composite risk = weighted sum                            │
│    → Example: 0.39 (medium-high risk)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. CALCULATE INTEGRITY SCORE (0-100 Quality)                   │
│    ├─ Data quality: NDVI, cloud cover, resolution → 30 pts     │
│    ├─ Model confidence: R² score → 20 pts                      │
│    ├─ Temporal stability: NDVI changes → 20 pts                │
│    ├─ Risk adjustment: Distance from threats → 15 pts          │
│    └─ Additionality: Prevents baseline emissions → 15 pts      │
│    → Example: 78.5 (high quality)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. DETERMINE PRICE (Market-based Algorithm)                    │
│    ├─ Base tier: integrity + risk → $12-35/tonne               │
│    ├─ Integrity bonus: (score-50)/100 × 8 → ±$4                │
│    ├─ Risk penalty: risk × 10 → -$0 to -$10                    │
│    └─ Final price = base + bonus - penalty (floor: $12)        │
│    → Example: $25.30/tonne                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. CREATE CARBON CREDIT                                        │
│    ├─ Save scan_results (biomass, indices, bands)              │
│    ├─ Create carbon_credits record:                            │
│    │   • quantity_tco2e: 1,481.4                               │
│    │   • price_per_tonne: $25.30                               │
│    │   • integrity_score: 78.5                                 │
│    │   • risk_score: 39.0                                      │
│    │   • status: "listed"                                      │
│    │   • vintage_year: 2026                                    │
│    └─ Credit value: 1,481.4 × $25.30 = $37,479                 │
│         Community receives: $22,487 (60%)                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Multi-source Data Integration:** Combines satellite imagery, climate data, and topography for comprehensive analysis

2. **Machine Learning Core:** Random Forest model trained on 10,000+ LiDAR measurements provides accurate biomass predictions

3. **IPCC-Compliant Carbon Accounting:** Uses internationally recognized conversion factors (47% carbon fraction, 3.667 CO₂/C ratio)

4. **Risk-Aware Pricing:** Automatically adjusts prices based on permanence risks and verification quality

5. **Transparent Pipeline:** Every step from satellite pixels to dollar price is documented and auditable

6. **Community-First:** 60% of credit value flows directly to local communities managing the land

---

## References

- **IPCC Guidelines for National Greenhouse Gas Inventories** (2006, 2019 Refinement)
- **GEDI L4B Biomass Product** - NASA EOSDIS
- **Sentinel-2 User Guide** - European Space Agency
- **Voluntary Carbon Market Standards** - Verra VCS, Gold Standard
- **Kenya Forest Service** - National forest cover data

---

**Document Version:** 1.0  
**Last Updated:** March 6, 2026  
**Platform:** Terrafoma Carbon Intelligence  
**Contact:** For technical questions about this pipeline

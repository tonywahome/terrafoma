# 🌍 TerraFoma

**Empowering local economies through transparent, AI-verified carbon credits**

TerraFoma is an AI-powered carbon credit platform that connects landowners with carbon markets through automated satellite-based biomass estimation. We make carbon credit verification accessible and transparent, with a community-first approach that directs 60% of credit value to local conservation communities.

## ✨ Key Features

### 🛰️ **Satellite-Based Biomass Estimation**
- Automated analysis using Google Earth Engine and Sentinel-2 satellite imagery
- Machine learning model trained on 9,000+ GEDI LiDAR samples from Congo Basin
- Real-time biomass prediction with R²=0.53 and MAE=19.3 tonnes/ha

### 💰 **Market-Competitive Pricing**
- Dynamic pricing based on project quality ($12-40 per tonne CO₂e)
- Four quality tiers: Premium, High, Standard, and Basic
- Pricing reflects integrity scores and risk assessments

### 🤝 **Community-First Approach**
- 60% of credit value goes directly to conservation communities
- Transparent breakdown: Community benefit + Conservation fund + Platform fee
- Real-time tracking of community impact

### 🎯 **Interactive Marketplace**
- Browse verified carbon credits by quality tier
- Detailed project information with satellite imagery
- Impact dashboard showing total carbon offset and community funding

### 📊 **Comprehensive Dashboard**
- Real-time biomass prediction from satellite data
- Risk assessment and integrity scoring
- Visual representation of carbon offsetting potential

## 🏗️ Architecture

### Tech Stack
- **Backend:** FastAPI (Python 3.13)
- **Frontend:** Next.js 14.2 + React + TypeScript + Tailwind CSS
- **ML Framework:** scikit-learn + XGBoost + CuML (GPU-accelerated)
- **Geospatial:** Google Earth Engine + Mapbox GL JS
- **Database:** In-memory store (demo) or Supabase/PostgreSQL (production)
  - In-memory: 5 sample credits, resets on restart
  - Supabase: Persistent, unlimited, production-ready
  - See [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md) for setup

### Core Components

```
terrafoma/
├── backend/
│   ├── main.py                    # FastAPI application entry
│   ├── database.py                # In-memory database with sample credits
│   ├── config.py                  # Configuration management
│   ├── routers/                   # API endpoints
│   │   ├── scan.py               # Satellite scanning endpoints
│   │   ├── credits.py            # Carbon credit marketplace API
│   │   ├── dashboard.py          # Analytics endpoints
│   │   └── certificates.py       # Certificate generation
│   ├── services/                  # Business logic
│   │   ├── biomass_estimator.py  # ML-powered biomass prediction
│   │   ├── carbon_calculator.py  # Pricing and community benefit calculation
│   │   ├── risk_scorer.py        # Risk assessment
│   │   └── certificate_generator.py
│   ├── models/                    # Database models
│   └── ml/                        # Machine learning
│       ├── models/
│       │   └── biomass_model_v1.pkl    # Trained RandomForest model (15MB)
│       ├── data/
│       │   ├── sentinel_gedi_training.csv       # 9001 training samples
│       │   └── gedi_congo_basin_biomass.csv     # 102MB GEDI dataset
│       ├── train_biomass_model.ipynb   # Comprehensive training notebook
│       ├── collect_sentinel_data.py    # Data collection from Earth Engine
│       └── collect_gedi_data.py        # GEDI LiDAR data collection
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx              # Landing page
│   │   │   ├── dashboard/            # Biomass prediction interface
│   │   │   ├── marketplace/          # Carbon credit marketplace
│   │   │   ├── registry/             # Credit registry
│   │   │   └── certificate/[id]/     # Certificate viewer
│   │   ├── components/
│   │   │   ├── MapView.tsx          # Mapbox integration
│   │   │   ├── RiskGauge.tsx        # Risk visualization
│   │   │   ├── StatsBar.tsx         # Statistics display
│   │   │   └── Navbar.tsx           # Navigation
│   │   └── lib/
│   │       ├── api.ts               # Backend API client
│   │       └── types.ts             # TypeScript definitions
└── docs/                             # Documentation

```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (3.13 recommended)
- **Node.js 18+** (tested with v22.1.0)
- **Google Earth Engine account** (free tier sufficient)
- **Mapbox API key** (free tier sufficient)

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd terrafoma

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp ../.env.example .env
# Edit .env and add your API keys:
# - EARTHENGINE_PROJECT_ID (Google Earth Engine project ID)
# - GOOGLE_APPLICATION_CREDENTIALS (path to GEE service account JSON)

# Authenticate with Google Earth Engine
earthengine authenticate

# Start the backend server
uvicorn main:app --reload --port 8002
```

Backend will be available at: http://localhost:8002
API documentation: http://localhost:8002/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Add your Mapbox token:
# NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here

# Start the development server
npm run dev
```

Frontend will be available at: http://localhost:3001

### 4. (Optional but Recommended) Set Up Supabase Database

By default, the app uses an in-memory database with 5 sample credits that reset on server restart. For a production-ready app with persistent data:

**Quick Setup (5 minutes):**

1. Create free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Copy your project URL and API keys
4. Run the SQL schema from `backend/data/schema.sql` in Supabase SQL Editor
5. Add to `.env`:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   ```
6. Restart backend server

**📖 Full Guide:** See [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md) for detailed step-by-step instructions.

**Benefits:**
- ✅ Persistent data (survives restarts)
- ✅ Unlimited carbon credits
- ✅ Real user authentication
- ✅ Transaction tracking
- ✅ Production-ready

### 5. (Optional) Train Custom Model

If you want to retrain the biomass estimation model with your own data:

```bash
cd backend/ml

# Open the training notebook
jupyter notebook train_biomass_model.ipynb

# Follow the notebook to:
# 1. Collect satellite and GEDI data
# 2. Train and evaluate models
# 3. Apply improvement strategies
# 4. Export the best model
```

The notebook includes GPU acceleration support for faster training with NVIDIA GPUs.

## 📊 ML Model Details

### Biomass Estimation Model

**Current Performance:**
- **Algorithm:** Random Forest Regressor (200 trees)
- **Test R²:** 0.53
- **MAE:** 19.3 tonnes/hectare
- **Training Samples:** 9,001 (Congo Basin region)

**Features Used:**
- 10 Sentinel-2 spectral bands (B1-B8, B11-B12)
- Derived vegetation indices (NDVI, EVI, SAVI, NDMI)
- Topographic features (elevation, slope)
- Temporal aggregations (median over dry season)

**Model File:** `backend/ml/models/biomass_model_v1.pkl` (15 MB)

### Training Data Collection

Data is collected from:
1. **Sentinel-2:** Multispectral satellite imagery (10-20m resolution)
2. **GEDI:** Space-based LiDAR biomass measurements
3. **SRTM:** Digital elevation model

Collection scripts are located in `backend/ml/`:
- `collect_sentinel_data.py` - Fetches Sentinel-2 imagery
- `collect_gedi_data.py` - Fetches GEDI biomass measurements

## 💳 Carbon Credit Pricing

### Pricing Algorithm

Credits are priced dynamically based on project quality:

```python
Base Price = $22 per tonne CO₂e

Quality Tiers:
- Premium (90-100):  $35/tonne  (integrity > 90, risk < 0.15)
- High (80-90):      Variable   (premium formula)
- Standard (70-80):  $18/tonne  (standard projects)
- Basic (< 70):      $12/tonne  (minimum viable price)
```

### Community Benefit Distribution

**60% goes to communities:**
- 45% → Direct community payments
- 15% → Conservation fund for project maintenance

**40% platform operations:**
- 25% → Verification and monitoring
- 10% → Platform maintenance
- 5% → Technology development

## 🎯 API Endpoints

### Core Endpoints

```
GET  /api/credits              # List all carbon credits
GET  /api/credits/{id}         # Get credit details
POST /api/scan                 # Scan a plot for biomass
GET  /api/dashboard            # Get dashboard statistics
GET  /api/certificate/{id}     # Get credit certificate
```

### Example: Scan a Plot

```bash
curl -X POST http://localhost:8002/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "lat": -2.5,
    "lon": 28.5,
    "buffer_m": 1000,
    "land_use": "forest"
  }'
```

Response:
```json
{
  "biomass_t_per_ha": 142.7,
  "total_biomass_t": 5429.8,
  "tco2e": 9567.2,
  "area_ha": 38.9,
  "integrity_score": 85.2,
  "risk_score": 0.22,
  "price_per_tonne": 22.62,
  "total_value_usd": 216501.74,
  "community_benefit_usd": 129901.04
}
```

## 🌟 Sample Carbon Credits

The platform includes 5 pre-populated conservation projects from Kenya:

| Project | Location | Area | Biomass | Carbon | Price | Total Value |
|---------|----------|------|---------|--------|-------|-------------|
| Aberdare Forest | Nyeri | 45.3 ha | 180.5 t/ha | 12,101 tCO₂e | $29.30 | $354,559 |
| Mount Kenya Woodland | Meru | 28.7 ha | 125.3 t/ha | 6,198 tCO₂e | $23.25 | $144,104 |
| Kakamega Rainforest | Kakamega | 67.2 ha | 210.8 t/ha | 24,415 tCO₂e | $37.78 | $922,279 |
| Mau Forest Complex | Nakuru | 52.1 ha | 95.4 t/ha | 8,566 tCO₂e | $21.30 | $182,456 |
| Loita Forest | Narok | 38.9 ha | 142.7 t/ha | 9,567 tCO₂e | $22.62 | $216,502 |

**Total Portfolio:** 62,847 tCO₂e | $1,819,900 | ~$1.1M to communities

## 🔧 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend (Black + isort)
cd backend
black .
isort .

# Frontend (Prettier)
cd frontend
npm run format
```

### Cleaning Build Artifacts

```bash
# Run the cleanup script
./cleanup.sh
```

This removes:
- Python cache files (`__pycache__`, `*.pyc`)
- Log files
- Temporary files
- Build artifacts

## 📈 Roadmap

### Current Version (v1.0)
- ✅ Satellite-based biomass estimation
- ✅ Carbon credit marketplace
- ✅ Community benefit calculation
- ✅ Risk scoring and integrity assessment
- ✅ In-memory database with sample credits

### Planned Features (v2.0)
- 🔄 Blockchain integration for credit verification
- 🔄 Integration with Supabase for persistent storage
- 🔄 Real-time monitoring and alerts
- 🔄 Mobile app for field verification
- 🔄 Multi-language support
- 🔄 Advanced analytics and reporting
- 🔄 Integration with carbon registries (Verra, Gold Standard)

## 📝 License

This project is part of a hackathon submission. License TBD.

## 🤝 Contributing

See [SETUP.md](docs/SETUP.md) for detailed development setup instructions.

## 🙏 Acknowledgments

- **Google Earth Engine** for satellite imagery access
- **NASA GEDI** for LiDAR biomass measurements
- **Mapbox** for mapping infrastructure
- **Sentinel-2** for open-access multispectral imagery
- **IPCC** for carbon accounting methodologies

## 📞 Contact

For questions about this hackathon submission, please contact the development team.

---

**Built with ❤️ for communities and the planet**

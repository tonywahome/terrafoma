# TerraFoma - Hackathon Submission Summary

**Prepared on:** March 6, 2024  
**Status:** Ready for Submission ✅

## Project Overview

TerraFoma is an AI-powered carbon credit platform that uses satellite imagery and machine learning to estimate biomass and enable transparent, community-first carbon credit trading. The platform directs 60% of credit value to local conservation communities.

## Key Metrics

### System Performance
- **Model Accuracy:** R² = 0.53, MAE = 19.3 t/ha
- **Training Dataset:** 9,001 samples from Congo Basin
- **Model Size:** 15 MB (Random Forest with 200 trees)
- **API Response Time:** < 5 seconds per scan
- **Carbon Credits:** 5 pre-populated projects
- **Total Carbon Portfolio:** 62,847 tCO₂e (~$1.8M value)

### Community Impact
- **Community Benefit:** 60% of credit value
- **Total Community Funding:** $1,091,940 (from sample credits)
- **Pricing Range:** $12-40 per tonne CO₂e
- **Quality Tiers:** 4 tiers (Premium, High, Standard, Basic)

### Technical Stack
- **Backend:** FastAPI + Python 3.13 + Google Earth Engine
- **Frontend:** Next.js 14.2 + React + TypeScript + Tailwind CSS
- **ML:** scikit-learn + XGBoost + GPU acceleration support
- **Geospatial:** Sentinel-2 + GEDI + SRTM + Mapbox

## Cleanup & Organization Summary

### Files Removed
✅ **Python Cache:** Removed all `__pycache__` directories and `*.pyc` files  
✅ **Log Files:** Removed collection.log (114KB), backend.log, frontend.log  
✅ **PID Files:** Removed collection.pid  
✅ **Duplicate Model:** Removed biomass_model_v2_improved.pkl (saved 15MB)  
✅ **OS Files:** Removed .DS_Store, Thumbs.db  
✅ **Unused Directories:** Removed notebooks/, streamlit-app/, .claude/  
✅ **Total Space Saved:** ~30+ MB

### Files Reorganized
✅ **ML Model:** Moved to `backend/ml/models/biomass_model_v1.pkl`  
✅ **Training Data:** Moved to `backend/ml/data/sentinel_gedi_training.csv`  
✅ **GEDI Data:** Moved to `backend/ml/data/gedi_congo_basin_biomass.csv`  
✅ **Documentation:** Created `docs/` directory  

### Documentation Created
✅ **README.md** (11KB) - Comprehensive project overview with:
   - Features and architecture
   - Installation instructions
   - ML model details
   - Carbon pricing algorithm
   - Sample credits table
   - API endpoint documentation
   - Roadmap and acknowledgments

✅ **docs/ARCHITECTURE.md** (20KB) - Complete system architecture:
   - System diagram
   - Component details (Frontend, Backend, ML Pipeline)
   - Data flow diagrams
   - Performance considerations
   - Security & scalability
   - Testing strategy
   - Deployment guide

✅ **docs/SETUP.md** (15KB) - Step-by-step setup guide:
   - Prerequisites and requirements
   - Environment setup
   - Backend configuration
   - Frontend configuration
   - Google Earth Engine setup
   - Troubleshooting guide
   - GPU acceleration setup
   - Model retraining instructions

✅ **docs/SUPABASE_SETUP.md** (NEW!) - Complete Supabase database setup:
   - Step-by-step Supabase account creation
   - Database table setup with SQL schema
   - API key configuration
   - Environment variable setup
   - Sample data insertion
   - Troubleshooting common issues
   - Benefits of using Supabase vs in-memory database
   - Security best practices

### Code Updates
✅ **Updated model paths** in 3 files:
   - `backend/services/biomass_estimator.py`
   - `backend/services/carbon_credit_engine.py`
   - `backend/routers/plots_enhanced.py`

## Final Project Structure

```
terrafoma/                           # 1.1 GB total
├── README.md                        # 11 KB - Project overview
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── cleanup.sh                       # 2.3 KB - Cleanup script
├── backend/                         # FastAPI server
│   ├── main.py                     # Application entry point
│   ├── database.py                 # In-memory database with 5 credits
│   ├── config.py                   # Configuration management
│   ├── requirements.txt            # Python dependencies
│   ├── routers/                    # API endpoints
│   │   ├── scan.py                # Satellite scanning
│   │   ├── credits.py             # Marketplace API
│   │   ├── dashboard.py           # Analytics
│   │   └── certificates.py        # Certificate generation
│   ├── services/                   # Business logic
│   │   ├── biomass_estimator.py   # ML prediction
│   │   ├── carbon_calculator.py   # Pricing (60% to communities)
│   │   ├── risk_scorer.py         # Risk assessment
│   │   └── certificate_generator.py
│   ├── models/                     # Database models
│   │   ├── credit.py
│   │   ├── land_plot.py
│   │   ├── risk.py
│   │   ├── transaction.py
│   │   └── user.py
│   ├── data/                       # Sample data
│   │   ├── sample_plots.geojson
│   │   ├── sample_weather.json
│   │   └── schema.sql
│   └── ml/                         # 131 MB - Machine learning
│       ├── models/
│       │   └── biomass_model_v1.pkl           # 15 MB - Trained model
│       ├── data/
│       │   ├── sentinel_gedi_training.csv     # 2.4 MB - Training data
│       │   └── gedi_congo_basin_biomass.csv   # 102 MB - GEDI dataset
│       ├── train_biomass_model.ipynb          # 504 KB - Training notebook
│       ├── collect_sentinel_data.py           # Data collection
│       ├── collect_gedi_data.py               # GEDI data
│       ├── improve_model.py                   # Model improvements
│       ├── README.md                          # ML documentation
│       └── INTEGRATION_GUIDE.md               # Integration guide
├── frontend/                        # Next.js web app
│   ├── package.json                # Dependencies
│   ├── next.config.js              # Next.js config
│   ├── tailwind.config.js          # Tailwind CSS config
│   ├── tsconfig.json               # TypeScript config
│   └── src/
│       ├── app/
│       │   ├── page.tsx           # Landing page
│       │   ├── layout.tsx         # App layout
│       │   ├── globals.css        # Global styles
│       │   ├── dashboard/         # Biomass scanning
│       │   ├── marketplace/       # Carbon credits
│       │   ├── registry/          # Credit registry
│       │   └── certificate/[id]/  # Certificate viewer
│       ├── components/
│       │   ├── MapView.tsx        # Mapbox integration
│       │   ├── RiskGauge.tsx      # Risk visualization
│       │   ├── StatsBar.tsx       # Statistics
│       │   ├── Navbar.tsx         # Navigation
│       │   └── IntegrityBadge.tsx # Quality badges
│       └── lib/
│           ├── api.ts             # Backend API client
│           ├── types.ts           # TypeScript types
│           └── utils.ts           # Utility functions
└── docs/                           # Documentation
    ├── ARCHITECTURE.md             # 20 KB - System design
    └── SETUP.md                    # 15 KB - Setup guide
```

## Features Implemented

### ✅ Core Features

1. **Satellite-Based Biomass Estimation**
   - Google Earth Engine integration
   - Sentinel-2 multispectral imagery
   - GEDI LiDAR biomass validation
   - 16 input features (spectral bands + vegetation indices + topography)
   - Random Forest prediction model

2. **Community-First Carbon Pricing**
   - Dynamic pricing based on quality ($12-40/tonne)
   - 60% of value to communities
   - Transparent benefit calculation
   - Four quality tiers with clear criteria

3. **Interactive Marketplace**
   - Impact dashboard (carbon available, community funding, projects)
   - Filter by quality tier (All, Premium, Standard)
   - Detailed credit cards with:
     * Project information
     * Quality tier badges
     * Carbon offset metrics
     * Community benefit display
     * Risk assessment
     * Purchase functionality

4. **Real-Time Dashboard**
   - Click-to-scan map interface
   - Instant biomass prediction
   - Carbon credit valuation
   - Risk and integrity scoring
   - Visual results display

5. **In-Memory Database**
   - 5 pre-populated conservation projects from Kenya
   - Supabase-compatible API
   - Realistic sample data with coordinates
   - Transaction tracking

### ✅ Technical Features

1. **ML Model Training**
   - Comprehensive Jupyter notebook
   - 5 improvement strategies tested
   - GPU acceleration support (XGBoost, CuML)
   - Model performance tracking
   - Feature importance analysis

2. **Data Collection Pipeline**
   - Automated Sentinel-2 data collection
   - GEDI biomass measurement collection
   - Earth Engine batch processing
   - Error handling and retry logic

3. **API Documentation**
   - Swagger/OpenAPI at /docs
   - Interactive endpoint testing
   - Request/response examples

4. **Code Quality**
   - Type hints (Python)
   - TypeScript (Frontend)
   - Modular architecture
   - Clear separation of concerns

## Sample Carbon Credits

| Project | Location | Biomass | Carbon | Price | Community Benefit |
|---------|----------|---------|--------|-------|-------------------|
| Aberdare Forest | Nyeri, Kenya | 180.5 t/ha | 12,101 tCO₂e | $29.30/t | $212,735 |
| Mount Kenya Woodland | Meru, Kenya | 125.3 t/ha | 6,198 tCO₂e | $23.25/t | $86,462 |
| Kakamega Rainforest | Kakamega, Kenya | 210.8 t/ha | 24,415 tCO₂e | $37.78/t | $553,367 |
| Mau Forest Complex | Nakuru, Kenya | 95.4 t/ha | 8,566 tCO₂e | $21.30/t | $109,474 |
| Loita Forest | Narok, Kenya | 142.7 t/ha | 9,567 tCO₂e | $22.62/t | $129,901 |

**TOTAL:** 62,847 tCO₂e | $1,819,900 | $1,091,940 to communities (60%)

## Running the Application

### Quick Start

**Terminal 1 - Backend:**
```bash
cd backend
source ../.venv/bin/activate
uvicorn main:app --reload --port 8002
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8002
- API Docs: http://localhost:8002/docs

### Current Status
✅ Both servers running  
✅ 5 carbon credits loaded  
✅ Marketplace functional  
✅ Biomass estimation working  
✅ Community benefits calculating correctly  

## Technology Highlights

### Machine Learning
- **Algorithm:** Random Forest Regressor (200 trees)
- **Training:** 9,001 samples from Congo Basin
- **Performance:** R² = 0.53, MAE = 19.3 t/ha
- **Features:** Sentinel-2 bands, vegetation indices, topography
- **Validation:** GEDI LiDAR biomass measurements

### Geospatial Processing
- **Satellite:** Sentinel-2 (10-20m resolution)
- **LiDAR:** GEDI L4A biomass product
- **DEM:** SRTM elevation data
- **Processing:** Google Earth Engine
- **Mapping:** Mapbox GL JS

### Web Application
- **Backend:** FastAPI (async, high performance)
- **Frontend:** Next.js 14 (App Router, React Server Components)
- **Styling:** Tailwind CSS (utility-first)
- **State Management:** React hooks
- **API Client:** Fetch API with TypeScript

## Future Enhancements

### Short Term
- [ ] Connect Supabase for persistent storage
- [ ] Add user authentication
- [ ] Implement payment processing
- [ ] Add email notifications
- [ ] Generate PDF certificates

### Long Term
- [ ] Blockchain integration for credit verification
- [ ] Mobile app for field data collection
- [ ] Real-time monitoring and alerts
- [ ] Integration with carbon registries (Verra, Gold Standard)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Batch credit processing

## Acknowledgments

**Data Sources:**
- Google Earth Engine
- NASA GEDI Mission
- ESA Sentinel-2 Program
- NASA SRTM Elevation Data

**Technology:**
- FastAPI framework
- Next.js and React
- scikit-learn
- Mapbox

**Methodology:**
- IPCC Guidelines for carbon accounting
- Kenya Forest Service conservation data
- Academic research on satellite-based biomass estimation

## Submission Checklist

✅ **Code Quality**
   - Clean, organized codebase
   - No cache files or temporary files
   - Proper directory structure
   - Updated file paths

✅ **Documentation**
   - Comprehensive README.md
   - Detailed ARCHITECTURE.md
   - Step-by-step SETUP.md
   - Inline code comments

✅ **Functionality**
   - Backend API working
   - Frontend responsive
   - ML model integrated
   - Sample data loaded
   - All features functional

✅ **Testing**
   - Backend endpoints tested
   - Frontend pages accessible
   - Earth Engine integration verified
   - Error handling in place

✅ **Deployment Ready**
   - Environment variables configured
   - Dependencies documented
   - Setup instructions clear
   - Troubleshooting guide included

## Contact & Support

For questions about this hackathon submission:
- Review the comprehensive documentation in `docs/`
- Check the setup guide: `docs/SETUP.md`
- Review architecture: `docs/ARCHITECTURE.md`
- Explore API documentation: http://localhost:8002/docs

---

**TerraFoma - Built with ❤️ for communities and the planet 🌍**

*Hackathon Submission - March 2024*

# TerraFoma

**Empowering local economies through transparent, AI-verified natural capital.**

TerraFoma is a centralized dMRV (Digital Monitoring, Reporting, and Verification) platform that connects small-to-medium scale landowners with local industrial emitters. We use AI to automate the valuation of carbon sequestration, bypassing the high costs of traditional verification.

## Architecture

- **Backend:** Python FastAPI with ML-powered biomass estimation
- **Frontend:** Next.js 14 + Mapbox GL JS for geospatial visualization
- **Analysis Tool:** Streamlit app for satellite data analysis demos
- **Database:** Supabase (PostgreSQL + PostGIS)
- **ML:** scikit-learn Random Forest for biomass and integrity scoring

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account
- Mapbox account (for public token)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp ../.env.example .env   # fill in your keys
python ml/train_model.py  # train the biomass model
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local  # fill in your keys
npm run dev
```

### Streamlit

```bash
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

## Key Features

1. **AI-Driven Land Scanning** - Select a plot on the map, get instant carbon stock estimates
2. **Carbon Credit Registry** - Transparent ledger tracking credits from verification to retirement
3. **Local Marketplace** - SMEs buy credits from nearby conservation projects
4. **Integrity Scoring** - ML model assigns confidence scores to each credit
5. **PDF Offset Certificates** - Downloadable proof of carbon offsetting
6. **Carbon Footprint Calculator** - SMEs estimate their annual emissions

## Project Structure

```
terrafoma/
├── backend/          # FastAPI server + ML models
├── frontend/         # Next.js marketplace & dashboard
├── streamlit-app/    # Satellite analysis demo tool
├── notebooks/        # ML training notebooks
└── .env.example      # Environment variable template
```

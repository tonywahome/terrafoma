# 🌍 TerraFoma

**Empowering local economies through transparent, AI-verified carbon credits**

TerraFoma is a comprehensive carbon credit platform that connects landowners directly with carbon markets through AI-powered satellite-based land analysis. Built with modern web technologies and machine learning, TerraFoma provides an end-to-end solution for carbon credit generation, verification, approval, and marketplace trading.

## 🎯 Project Overview

TerraFoma bridges the gap between landowners and carbon markets by:
- **Automated Verification**: AI-powered satellite analysis using Google Earth Engine
- **Direct Connection**: Landowners register land → Admin verifies → Landowner approves → Instant marketplace listing
- **Transparent Pricing**: Dynamic pricing based on quality metrics ($12-40 per tonne CO₂e)
- **Real-time Tracking**: Complete workflow management with notifications and dashboard analytics

## 📑 Table of Contents

- [Key Features](#-key-features)
- [User Workflows](#-user-workflows)
- [Technology Stack & Architecture](#-technology-stack--architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Database Schema](#-database-schema)
- [Machine Learning Model](#-machine-learning-model)
- [API Endpoints](#-api-endpoints)
- [Carbon Credit Pricing](#-carbon-credit-pricing)
- [Development](#-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Key Technologies](#-key-technologies)
- [Roadmap](#-roadmap)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Contact](#-contact)

## ✨ Key Features

### � **Multi-Role System**
- **Landowners**: Register land with interactive map polygon drawing, receive notifications for scans, approve/reject carbon credit listings
- **Admin**: Review registration requests, perform AI-powered land scans, manage system operations through comprehensive dashboard
- **Business**: Browse marketplace, purchase carbon credits, track carbon offset impact

### 🗺️ **Interactive Land Registration**
- Draw land boundaries directly on satellite map using Mapbox
- Automatic area calculation from polygon coordinates
- Geometry data captured and stored for precise scanning
- Admin receives requests with pre-loaded land boundaries

### 🛰️ **AI-Powered Satellite Analysis**
- Automated biomass estimation using Google Earth Engine and Sentinel-2 imagery
- Machine learning model trained on 9,000+ GEDI LiDAR samples from Congo Basin
- Real-time predictions with R²=0.53 and MAE=19.3 tonnes/ha
- Generates carbon credits with integrity scoring and risk assessment

### 🔔 **Complete Notification System**
- Real-time notifications for landowners when scans are complete
- Approval workflow: Landowners review scan results before marketplace listing
- Confirmation notifications after approval/rejection decisions
- Notification center with unread counts and filtering

### 🏪 **Dynamic Carbon Marketplace**
- Browse verified carbon credits by status (listed, sold, retired)
- Quality-based pricing tiers: Premium ($35), Standard ($18), Basic ($12)
- Detailed project information with satellite imagery and location data
- Filter and sort by price, quantity, integrity score
- Integrated payment processing with Polar.sh

### 📊 **Comprehensive Dashboards**

**Admin Dashboard:**
- Registration request statistics and status tracking
- Carbon credit metrics (total, pending approval, listed, sold)
- System health monitoring
- Quick access to common operations
- Visual charts for data distribution

**Business Dashboard:**
- Global emissions tracking and carbon footprint calculator
- Credit marketplace overview
- Portfolio management
- Impact measurement tools

**Landowner Dashboard:**
- Pending scan notifications
- Approval/rejection interface
- Transaction history
- Credit status tracking

## 🔄 User Workflows

### Landowner Journey
1. **Register**: Sign up and draw land boundaries on interactive map
2. **Submit**: Submit registration request with land details (location, size, type, geometry)
3. **Wait**: Admin reviews and processes the request
4. **Notification**: Receive notification when admin completes AI scan
5. **Review**: View scan results (biomass, carbon stock, potential credits, pricing)
6. **Approve/Reject**: Accept to list credit on marketplace or reject with reason
7. **Confirm**: Receive confirmation notification of approval decision
8. **Track**: Monitor credit status and transactions through dashboard

### Admin Journey
1. **Review Requests**: View pending land registration requests
2. **Auto-Scan**: Click to scan - land geometry pre-loaded from landowner submission
3. **AI Analysis**: System performs satellite-based biomass estimation
4. **Generate Credit**: Carbon credit created with "pending_approval" status
5. **Notify**: Landowner automatically notified of scan completion
6. **Monitor**: Track approval workflow through admin dashboard
7. **Manage**: View system statistics and pending approvals

### Business Journey
1. **Browse**: Explore marketplace for available carbon credits
2. **Filter**: Sort by price, quality, location, quantity
3. **Review**: View detailed project information and satellite imagery
4. **Purchase**: Integrated checkout with Polar.sh payment processing
5. **Track**: Monitor carbon offset impact through dashboard
6. **Certificate**: Receive digital verification certificate

## 🏗️ Architecture

### Tech Stack
- **Backend:** FastAPI (Python 3.13) with async/await
- **Frontend:** Next.js 14.2 + React 18 + TypeScript 5.7
- **Styling:** Tailwind CSS 3.4 with custom theme
- **ML Framework:** scikit-learn + XGBoost for biomass prediction
- **Geospatial:** 
  - Google Earth Engine for satellite imagery analysis
  - Mapbox GL JS 3.9 + Mapbox Draw 1.5 for interactive mapping
  - PostGIS for geometry storage
- **Database:** Supabase (PostgreSQL) with Row-Level Security (RLS)
- **Authentication:** Custom auth system with role-based access control (RBAC)
- **Payment:** Polar.sh SDK integration for carbon credit purchases
- **Charts:** Recharts for data visualization
- **API Documentation:** OpenAPI/Swagger (auto-generated)

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Landowner│  │  Admin   │  │ Business │  │ Public   │   │
│  │Dashboard │  │Dashboard │  │Dashboard │  │ Landing  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       └────────┬────┴─────────────┬──────────────┘         │
│                │    API Client     │                        │
└────────────────┼───────────────────┼────────────────────────┘
                 │                   │
┌────────────────▼───────────────────▼────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   API Routers                         │  │
│  │  • auth.py         • scan.py        • credits.py     │  │
│  │  • registration.py • landowner.py   • dashboard.py   │  │
│  │  • notifications.py • transactions.py • plots.py     │  │
│  └──────┬───────────────────────────────────────────────┘  │
│         │                                                    │
│  ┌──────▼────────────────────────────────────────────────┐ │
│  │                 Business Logic Services                │ │
│  │  • biomass_estimator.py   • carbon_calculator.py     │ │
│  │  • risk_scorer.py         • certificate_generator.py │ │
│  │  • location_service.py    • gee_feature_extractor.py │ │
│  └──────┬────────────────────────────────────────────────┘ │
│         │                                                    │
│  ┌──────▼────────────────────────────────────────────────┐ │
│  │          ML Model (RandomForest)                      │  │
│  │      biomass_model_v1.pkl (15MB)                      │  │
│  │      R²=0.53, MAE=19.3 t/ha                           │  │
│  └──────┬────────────────────────────────────────────────┘ │
└─────────┼────────────────────────────────────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────────┐
│              External Services                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  Supabase   │  │   Google    │  │   Mapbox    │       │
│  │ PostgreSQL  │  │    Earth    │  │  Tile API   │       │
│  │   + RLS     │  │   Engine    │  │             │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└────────────────────────────────────────────────────────────┘
```

### Project Structure

```
terrafoma/
├── backend/
│   ├── main.py                         # FastAPI application entry
│   ├── database.py                     # Supabase client with admin bypass for RLS
│   ├── config.py                       # Environment configuration
│   │
│   ├── routers/                        # API endpoint handlers
│   │   ├── auth.py                    # User authentication & registration
│   │   ├── registration.py            # Land registration requests
│   │   ├── scan.py                    # AI satellite scanning
│   │   ├── landowner.py               # Landowner approval workflow
│   │   ├── notifications.py           # Real-time notification system
│   │   ├── credits.py                 # Carbon credit marketplace
│   │   ├── transactions.py            # Purchase/sale tracking
│   │   ├── dashboard.py               # Analytics endpoints
│   │   ├── plots.py                   # Land plot management
│   │   └── certificates.py            # Certificate generation
│   │
│   ├── services/                       # Business logic layer
│   │   ├── biomass_estimator.py       # ML-powered biomass prediction
│   │   ├── gee_feature_extractor.py   # Google Earth Engine integration
│   │   ├── carbon_calculator.py       # Pricing & benefit calculation
│   │   ├── risk_scorer.py             # Project risk assessment
│   │   ├── location_service.py        # Geocoding & location services
│   │   ├── certificate_generator.py   # PDF certificate generation
│   │   └── mock_data.py              # Sample data generator
│   │
│   ├── models/                         # Pydantic data models
│   │   ├── user.py                    # User & authentication models
│   │   ├── land_plot.py               # Land plot schemas
│   │   ├── credit.py                  # Carbon credit models
│   │   ├── transaction.py             # Transaction models
│   │   └── risk.py                    # Risk assessment models
│   │
│   ├── ml/                             # Machine learning pipeline
│   │   ├── models/
│   │   │   └── biomass_model_v1.pkl   # Trained model (15MB, R²=0.53)
│   │   ├── data/
│   │   │   └── sentinel_gedi_training.csv  # 9,001 training samples
│   │   ├── train_biomass_model.ipynb  # Model training notebook
│   │   ├── collect_sentinel_data.py   # Data collection scripts
│   │   └── collect_gedi_data.py       # GEDI LiDAR data fetcher
│   │
│   ├── data/                           # Database schemas & migrations
│   │   ├── schema.sql                 # Complete database schema
│   │   ├── migration_add_auth.sql     # Auth system migration
│   │   ├── migration_approval_workflow.sql  # Approval workflow
│   │   └── sample_data.sql            # Sample credits & users
│   │
│   └── requirements.txt                # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/                        # Next.js 14 App Router
│   │   │   ├── page.tsx               # Landing page with hero
│   │   │   ├── login/                 # Authentication pages
│   │   │   ├── admin/
│   │   │   │   ├── dashboard/         # Admin analytics dashboard
│   │   │   │   └── requests/          # Registration review
│   │   │   ├── landowner/
│   │   │   │   ├── page.tsx           # Landowner dashboard
│   │   │   │   └── pending-scans/     # Approval interface
│   │   │   ├── dashboard/             # Business dashboard
│   │   │   ├── marketplace/           # Carbon credit marketplace
│   │   │   ├── registry/              # Public credit registry
│   │   │   ├── scan/                  # Satellite scan interface
│   │   │   ├── request-registration/  # Land registration form
│   │   │   └── certificate/[id]/      # Certificate viewer
│   │   │
│   │   ├── components/                 # Reusable React components
│   │   │   ├── Navbar.tsx             # Role-based navigation
│   │   │   ├── ProtectedRoute.tsx     # Auth guard component
│   │   │   ├── MapView.tsx            # Mapbox map integration
│   │   │   ├── RiskGauge.tsx          # Risk visualization gauge
│   │   │   ├── StatsBar.tsx           # Statistics display bar
│   │   │   └── CreditCard.tsx         # Credit listing card
│   │   │
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx        # Global auth state
│   │   │
│   │   └── lib/
│   │       ├── api.ts                 # Type-safe API client
│   │       └── types.ts               # TypeScript interfaces
│   │
│   ├── public/                         # Static assets
│   ├── package.json                    # Node dependencies
│   ├── tailwind.config.js             # Tailwind customization
│   └── tsconfig.json                   # TypeScript config
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                # System architecture
│   ├── SETUP.md                       # Development setup guide
│   ├── SUPABASE_SETUP.md             # Database setup instructions
│   └── SUPABASE_QUICK_START.md       # Quick start guide
│
├── .env.example                        # Environment variables template
├── .gitignore                         # Git ignore patterns
└── README.md                          # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (3.13 recommended)
- **Node.js 18+** (22.1.0 recommended)
- **Google Earth Engine account** ([sign up free](https://earthengine.google.com/))
- **Mapbox account** ([get free API key](https://account.mapbox.com/))
- **Supabase account** ([create free project](https://supabase.com/))

### Quick Start (15 minutes)

#### 1. Clone Repository

```bash
git clone https://github.com/tonywahome/terrafoma.git
cd terrafoma
```

#### 2. Set Up Supabase Database

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com/) and create account
   - Create new project (wait ~2 minutes for setup)
   - Copy your project URL and API keys

2. **Run Database Schema**
   - Open Supabase SQL Editor
   - Copy contents of `backend/data/schema.sql`
   - Execute to create all tables, RLS policies, and functions

3. **Load Sample Data** (Optional)
   - Execute `backend/data/sample_data.sql` for demo credits
   - Creates 30 sample credits across different statuses
   - Includes test users (landowner, business, admin)

**📖 Detailed Guide:** See [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)

#### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv ../.venv
source ../.venv/bin/activate  # Windows: ..\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
```

Edit `.env` and add your credentials:
```env
# Supabase (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Google Earth Engine (Required for scanning)
EARTHENGINE_PROJECT_ID=your-gee-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

```bash
# Authenticate with Google Earth Engine
earthengine authenticate

# Start backend server
uvicorn main:app --reload --port 8002
```

✅ Backend running at: http://localhost:8002  
📚 API Documentation: http://localhost:8002/docs

#### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here

# Polar.sh Payment Integration (Optional)
NEXT_PUBLIC_POLAR_SERVER=sandbox
NEXT_PUBLIC_POLAR_ACCESS_TOKEN=your_polar_token
NEXT_PUBLIC_POLAR_PRODUCT_ID=your_product_id
```

```bash
# Start development server
npm run dev
```

✅ Frontend running at: http://localhost:3001

### User Accounts

The system supports three user roles. Create accounts through the registration page or use sample data:

**Test Credentials** (if you loaded sample_data.sql):
```
Landowner:
  Email: orpheus@terrafoma.com
  Password: password123
  
Admin:
  Email: admin@terrafoma.com
  Password: admin123
  
Business:
  Email: business@terrafoma.com
  Password: business123
```

### First Steps

1. **As Landowner:**
   - Register your account
   - Navigate to "Register Land"
   - Draw your land boundaries on the map
   - Submit registration request

2. **As Admin:**
   - Log in with admin credentials
   - Go to "Registrations" to review requests
   - Click "Auto Scan with Geometry" to analyze land
   - System creates carbon credit and notifies landowner

3. **As Landowner (Approval):**
   - Check "Dashboard" for notification
   - Click notification to view scan results
   - Approve or reject the carbon credit listing

4. **As Business:**
   - Browse "Marketplace" for available credits
   - View credit details and project information
   - Purchase credits (Polar.sh integration)

## �️ Database Schema

The Supabase PostgreSQL database includes:

### Tables
- **`users`**: User accounts with role-based access (admin, landowner, business)
- **`registration_requests`**: Land registration submissions with geometry data
- **`land_plots`**: Verified land parcels with geospatial data
- **`scan_results`**: AI scanning results with biomass estimates
- **`carbon_credits`**: Carbon credits with status workflow (pending_approval → listed → sold → retired)
- **`notifications`**: Real-time notification system for users
- **`transactions`**: Purchase and sale tracking
- **`audit_log`**: System activity logging

### Key Features
- **Row-Level Security (RLS)**: Automatic data access control based on user role
- **PostGIS Extension**: Geospatial queries for land parcels
- **Automatic Timestamps**: `created_at` and `updated_at` fields
- **Foreign Key Constraints**: Referential integrity
- **Indexes**: Optimized queries on frequently accessed fields

### Credit Status Workflow
```
Registration → Scan → pending_approval → listed → sold/retired
                              ↓
                         (Landowner Approval Required)
```

## 📊 ML Model Details

### Biomass Estimation Model

**Algorithm:** Random Forest Regressor (200 trees)

**Performance Metrics:**
- **Test R²:** 0.53 (Explains 53% of variance)
- **MAE:** 19.3 tonnes/hectare (Mean Absolute Error)
- **RMSE:** 27.8 tonnes/hectare
- **Training Samples:** 9,001 from Congo Basin region
- **Model Size:** 15 MB (serialized with pickle)

**Input Features (18 total):**
- **Spectral Bands** (10): Sentinel-2 B1-B8, B11-B12
- **Vegetation Indices** (4): NDVI, EVI, SAVI, NDMI
- **Topographic** (2): Elevation, Slope
- **Temporal**: Median aggregation over dry season (reduces cloud interference)

**Training Data Sources:**
1. **Sentinel-2 L2A**: 10-20m resolution multispectral imagery
2. **GEDI L4A**: Space-based LiDAR biomass measurements (1km footprints)
3. **SRTM DEM**: 30m resolution elevation data

**Model File:** `backend/ml/models/biomass_model_v1.pkl`

### Data Collection Pipeline

Scripts for collecting training data:
- `collect_sentinel_data.py`: Fetches Sentinel-2 features via Google Earth Engine
- `collect_gedi_data.py`: Downloads GEDI biomass measurements
- Training data: `backend/ml/data/sentinel_gedi_training.csv` (9,001 samples)

### Retraining the Model

The Jupyter notebook `train_biomass_model.ipynb` provides:
- Data preprocessing and feature engineering
- Model selection (comparing RF, XGBoost, Linear)
- Hyperparameter tuning with GridSearchCV
- Cross-validation and performance evaluation
- GPU acceleration support with CuML (NVIDIA)
- Model export and versioning

## 🎯 API Endpoints

### Authentication
```
POST /api/auth/register      # Create new user account
POST /api/auth/login         # Authenticate and get user session
GET  /api/auth/me            # Get current user profile
```

### Land Registration
```
GET  /api/registration/requests              # List all requests (admin)
GET  /api/registration/requests?status=pending  # Filter by status
POST /api/registration/request               # Submit registration (landowner)
```

### Scanning & Credits
```
POST /api/scan                     # Perform AI satellite scan (admin)
GET  /api/credits                  # List all carbon credits
GET  /api/credits?status=listed    # Filter by status
GET  /api/credits/{id}             # Get credit details
GET  /api/credits/stats            # Get marketplace statistics
```

### Landowner Workflow
```
GET  /api/landowner/pending-scans  # Get scans awaiting approval
POST /api/landowner/approve-listing # Approve/reject carbon credit
```

### Notifications
```
GET  /api/notifications?user_id={id}  # Get user notifications
POST /api/notifications/{id}/read     # Mark as read
GET  /api/notifications/unread-count  # Get unread count
```

### Marketplace & Transactions
```
GET  /api/credits?status=listed    # Browse marketplace
POST /api/transactions             # Purchase carbon credit
GET  /api/transactions/history     # Get purchase history
```

### Dashboard Analytics
```
GET  /api/dashboard/footprint      # Calculate carbon footprint
GET  /api/credits/stats            # Get credit statistics
```

### Example: Scan Land Parcel

**Request:**
```bash
curl -X POST http://localhost:8002/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "plot_id": "uuid-of-land-plot",
    "request_id": "uuid-of-registration-request",
    "lat": -2.5,
    "lon": 28.5,
    "buffer_m": 1000,
    "land_use": "forest",
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[28.5, -2.5], [28.51, -2.5], ...]]
    }
  }'
```

**Response:**
```json
{
  "scan_id": "uuid-of-scan",
  "credit_id": "uuid-of-credit",
  "biomass_t_per_ha": 142.7,
  "total_biomass_t": 5429.8,
  "tco2e": 9567.2,
  "area_ha": 38.9,
  "integrity_score": 85.2,
  "risk_score": 0.22,
  "price_per_tonne": 22.62,
  "total_value_usd": 216501.74,
  "status": "pending_approval",
  "notification_sent": true
}
```

## 💳 Carbon Credit Pricing

### Dynamic Pricing Algorithm

Credits are priced based on quality metrics to ensure market competitiveness and fairness:

```python
Base Price = $22 per tonne CO₂e

Quality Tiers:
┌─────────────┬──────────────────┬──────────────┬──────────────┐
│    Tier     │   Integrity      │ Risk Score   │ Price/tonne  │
├─────────────┼──────────────────┼──────────────┼──────────────┤
│ Premium     │    ≥ 90          │   < 0.15     │    $35       │
│ High        │   80-89          │   0.15-0.25  │  $22-35      │
│ Standard    │   70-79          │   0.25-0.40  │    $18       │
│ Basic       │    < 70          │    > 0.40    │    $12       │
└─────────────┴──────────────────┴──────────────┴──────────────┘
```

### Pricing Factors

**Integrity Score (0-100):**
- Baseline MRV quality (40%)
- Permanence assurance (30%)
- Leakage risk mitigation (30%)

**Risk Score (0-1):**
- Political/regulatory stability
- Land tenure security
- Environmental monitoring capability
- Community support strength

### Value Distribution

**Revenue Allocation Example:**
```
Sale Price: $22/tonne × 1,000 tCO₂e = $22,000

Landowner:        $13,200  (60%)
Conservation Fund: $3,300  (15%)
Platform Fee:      $5,500  (25%)
──────────────────────────────────
Total:            $22,000  (100%)
```

## 🔧 Development

### Running the Project

**Development Mode:**
```bash
# Terminal 1: Backend
cd backend
source ../.venv/bin/activate
uvicorn main:app --reload --port 8002

# Terminal 2: Frontend  
cd frontend
npm run dev
```

**Production Build:**
```bash
# Backend
cd backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002

# Frontend
cd frontend
npm run build
npm start
```

### Environment Variables

**Backend (.env):**
```env
# Database (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Google Earth Engine (Required for scanning)
EARTHENGINE_PROJECT_ID=your-gee-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Optional: Logging
LOG_LEVEL=INFO
```

**Frontend (.env.local):**
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8002

# Mapbox (Required for maps)
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token

# Polar.sh Payment Integration (Optional)
NEXT_PUBLIC_POLAR_SERVER=sandbox
NEXT_PUBLIC_POLAR_ACCESS_TOKEN=your_polar_token
NEXT_PUBLIC_POLAR_PRODUCT_ID=your_product_id
NEXT_PUBLIC_POLAR_WEBHOOK_SECRET=your_webhook_secret
```

### Code Quality

**Python Linting:**
```bash
cd backend
black .                  # Format code
isort .                  # Sort imports
flake8 .                 # Check style
mypy .                   # Type checking
```

**TypeScript Checking:**
```bash
cd frontend
npm run lint             # ESLint
npm run type-check       # TypeScript compiler
npm run format           # Prettier
```

### Testing

```bash
# Backend unit tests
cd backend
pytest tests/ -v

# Frontend component tests
cd frontend
npm test

# End-to-end tests
npm run test:e2e
```

## 🚀 Deployment

### Backend Deployment (Railway/Render/Fly.io)

1. **Configure environment variables** in your platform dashboard
2. **Set build command**: `pip install -r requirements.txt`
3. **Set start command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Deploy** from GitHub repository

### Frontend Deployment (Vercel/Netlify)

1. **Connect GitHub repository**
2. **Set framework**: Next.js
3. **Set build command**: `npm run build`
4. **Set output directory**: `.next`
5. **Add environment variables** from .env.local
6. **Deploy**

### Database (Supabase)

Already production-ready! Free tier includes:
- 500 MB database storage
- 2 GB file storage
- 50 MB bandwidth
- Row-Level Security (RLS)
- Automatic backups

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check port availability
lsof -ti:8002 | xargs kill -9  # macOS/Linux
```

**Frontend build errors:**
```bash
# Clear cache
rm -rf .next node_modules package-lock.json

# Reinstall
npm install

# Check Node version
node --version  # Should be 18+
```

**Google Earth Engine authentication:**
```bash
# Re-authenticate
earthengine authenticate

# Verify credentials
earthengine asset info users/your-username
```

**Supabase connection issues:**
- Verify URL and keys in .env
- Check project is active in Supabase dashboard
- Ensure RLS policies are enabled
- Check network/firewall settings

**Map not loading:**
- Verify NEXT_PUBLIC_MAPBOX_TOKEN in .env.local
- Check Mapbox account is active
- Ensure token has correct scopes

### Getting Help

1. Check [documentation](docs/) folder
2. Review [API documentation](http://localhost:8002/docs) when backend running
3. Check browser console for frontend errors
4. Check backend logs for API errors
5. Verify all environment variables are set correctly

## 🎨 Key Technologies

### Frontend Stack
- **Next.js 14.2**: React framework with App Router, Server Components, and API routes
- **React 18**: Component library with hooks and context API
- **TypeScript 5.7**: Type-safe development with strict mode
- **Tailwind CSS 3.4**: Utility-first styling with custom design system
- **Mapbox GL JS 3.9**: Interactive mapping with satellite imagery
- **Mapbox Draw 1.5**: Polygon drawing for land boundaries
- **Recharts**: Responsive data visualization (pie, bar, area charts)
- **React Hook Form**: Form validation and state management

### Backend Stack
- **FastAPI 0.115**: Modern async Python web framework
- **Pydantic**: Data validation and serialization
- **Supabase Client**: PostgreSQL database with realtime subscriptions
- **Google Earth Engine**: Satellite imagery analysis platform
- **scikit-learn**: Machine learning model (RandomForest)
- **Joblib**: Model serialization and loading
- **Geopy**: Geocoding and reverse geocoding
- **NumPy**: Numerical computing for ML features

### DevOps & Tools
- **Git**: Version control with GitHub
- **npm/pip**: Package management
- **ESLint/Black**: Code linting and formatting
- **Uvicorn**: ASGI server for FastAPI
- **Node.js**: JavaScript runtime for Next.js

## 📐 Architecture Highlights

### Smart Design Decisions

1. **Row-Level Security (RLS) Bypass Pattern**
   - Admin operations use service role key to bypass RLS
   - Ensures notifications reach all users regardless of RLS policies
   - Pattern: `get_admin_client()` for privileged operations

2. **Geometry Data Flow**
   - Landowners draw polygons → Stored as GeoJSON in PostgreSQL
   - Admin loads pre-drawn geometry → Auto-fills scan interface
   - No manual coordinate entry required

3. **Async/Await Architecture**
   - FastAPI endpoints use async for better performance
   - Non-blocking I/O for database queries
   - Concurrent request handling

4. **Type Safety Across Stack**
   - Python: Pydantic models with strict validation
   - TypeScript: Interfaces and types for all API responses
   - Reduced runtime errors through compile-time checks

5. **Status-Driven Workflow**
   - Carbon credits follow state machine pattern
   - Clear transitions: pending_approval → listed → sold → retired
   - Database constraints enforce valid state transitions

## 🌟 Project Highlights

### What Makes TerraFoma Unique

✅ **Complete End-to-End Solution**
- Not just a marketplace or scanner, but full workflow from registration to sale

✅ **AI-Powered Verification**
- Machine learning model trained on real satellite and LiDAR data
- Reduces verification costs from thousands to near-zero

✅ **User-Centric Design**
- Three distinct role-based interfaces (landowner, admin, business)
- Interactive map-based land registration (draw your boundaries)
- Real-time notifications and approval workflow

✅ **Production-Ready Architecture**
- Supabase integration for scalable, persistent storage
- Row-Level Security for data protection
- Admin bypass patterns for system operations

✅ **Modern Tech Stack**
- Latest versions of Next.js, React, FastAPI
- TypeScript throughout for type safety
- Responsive design with Tailwind CSS

✅ **Transparent Pricing**
- Quality-based dynamic pricing algorithm
- Clear value distribution (60% to landowners)
- Market-competitive rates ($12-40/tonne)

### Technical Achievements

🔬 **Machine Learning**
- Successfully trained biomass model on 9,001 samples
- R²=0.53 performance on test set
- Real-time predictions in < 5 seconds

🗺️ **Geospatial Integration**
- Google Earth Engine API for satellite imagery
- Mapbox for interactive mapping
- PostGIS for geometry storage and queries

🔔 **Real-Time System**
- Notification system with instant delivery
- Status updates propagate through dashboard
- Approval workflow with confirmation loop

🔐 **Security**
- Role-based access control (RBAC)
- Row-Level Security in database
- Admin bypass for system operations
- Environment variable configuration for secrets

## 📈 Project Stats

- **Lines of Code**: ~15,000
- **API Endpoints**: 25+
- **Database Tables**: 8
- **React Components**: 30+
- **ML Model Size**: 15 MB
- **Training Samples**: 9,001
- **Supported Roles**: 3 (Admin, Landowner, Business)
- **Development Time**: Sprint-based implementation

## 📈 Roadmap

### Current Version (v1.0) ✅

- ✅ Three-role user system (Admin, Landowner, Business)
- ✅ Interactive land registration with Mapbox polygon drawing
- ✅ Admin review and approval workflow
- ✅ AI-powered satellite scanning with Google Earth Engine
- ✅ Trained biomass estimation model (R²=0.53)
- ✅ Landowner notification and approval system
- ✅ Dynamic carbon credit pricing ($12-40/tonne)
- ✅ Complete marketplace with filtering and sorting
- ✅ Comprehensive dashboards for all user roles
- ✅ Supabase integration with Row-Level Security
- ✅ Payment integration with Polar.sh
- ✅ Certificate generation and verification
- ✅ Transaction tracking and history
- ✅ Responsive design for all screen sizes

### Planned Features (v2.0) 🔄

**Enhanced Verification:**
- 🔄 Blockchain integration for immutable credit verification
- 🔄 Integration with Verra and Gold Standard registries
- 🔄 Multi-temporal monitoring for additionality verification
- 🔄 Automated change detection from satellite imagery

**Mobile Experience:**
- 🔄 Progressive Web App (PWA) for offline access
- 🔄 Native mobile apps (iOS/Android) for field verification
- 🔄 GPS-based boundary capture directly from phone
- 🔄 Photo upload capability for ground-truthing

**Advanced Analytics:**
- 🔄 Predictive analytics for credit pricing trends
- 🔄 Portfolio optimization recommendations
- 🔄 Carbon offset impact visualization
- 🔄 ESG reporting dashboard for businesses

**Platform Expansion:**
- 🔄 Multi-language support (French, Spanish, Portuguese)
- 🔄 Support for additional ecosystems (mangroves, wetlands, grasslands)
- 🔄 Community marketplace for direct landowner-to-business trading
- 🔄 API for third-party integration

**AI/ML Improvements:**
- 🔄 Ensemble model with XGBoost and Neural Networks
- 🔄 Region-specific models for better accuracy
- 🔄 Real-time model retraining with new GEDI data
- 🔄 Uncertainty quantification for predictions

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)**: Detailed development setup guide
- **[SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)**: Step-by-step database setup
- **[SUPABASE_QUICK_START.md](docs/SUPABASE_QUICK_START.md)**: Quick reference guide
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture details
- **API Docs**: Auto-generated at http://localhost:8002/docs

## 🤝 Contributing

This project was built for demonstration and evaluation purposes. Contributions, issues, and feature requests are welcome!

**Development Workflow:**
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Code Standards:**
- Follow existing code style and patterns
- Add TypeScript types for all new code
- Include docstrings for Python functions
- Test all changes before submitting
- Update documentation for new features

## 📝 License

This project is part of a hackathon/demonstration submission. All rights reserved.

For commercial use or licensing inquiries, please contact the project maintainers.

## 🙏 Acknowledgments

### Data & Infrastructure
- **[Google Earth Engine](https://earthengine.google.com/)**: Petabyte-scale satellite imagery and geospatial analysis
- **[NASA GEDI](https://gedi.umd.edu/)**: Spaceborne LiDAR biomass measurements
- **[ESA Sentinel-2](https://sentinel.esa.int/)**: Free, open-access multispectral satellite imagery
- **[Mapbox](https://www.mapbox.com/)**: Interactive mapping and visualization
- **[Supabase](https://supabase.com/)**: PostgreSQL database with realtime capabilities

### Scientific Foundation
- **IPCC Guidelines**: Carbon accounting methodologies
- **UNFCCC**: Framework for carbon credit standards
- **Verra VCS**: Standards for project verification
- **FAO Global Forest Resources**: Reference data for biomass allometry

### Technology Stack
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern Python web framework
- **[Next.js](https://nextjs.org/)**: React framework by Vercel
- **[Tailwind CSS](https://tailwindcss.com/)**: Utility-first CSS framework
- **[scikit-learn](https://scikit-learn.org/)**: Machine learning in Python

### Community
- Thank you to all open-source contributors whose work made this project possible
- Special thanks to the Earth observation and carbon markets communities

## 👨‍💻 Team

Built with ❤️ by developers passionate about climate action and technology.

## 📞 Contact

For questions, feedback, or collaboration opportunities:
- **GitHub**: [@tonywahome](https://github.com/tonywahome)
- **Repository**: [TerraFoma](https://github.com/tonywahome/terrafoma)
- **Email**: [Contact through GitHub]

---

<div align="center">

**🌍 Built for the planet, powered by technology 🌿**

*Making carbon markets accessible, transparent, and impactful*

[Demo](http://localhost:3001) · [Documentation](docs/) · [API](http://localhost:8002/docs) · [Report Bug](https://github.com/tonywahome/terrafoma/issues)

</div>

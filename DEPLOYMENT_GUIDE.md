# 🚀 TerraFoma Deployment Guide

## 📋 Overview

**Recommended Architecture:**
- **Frontend**: Vercel (optimized for Next.js)
- **Backend**: Railway or Render (easy Python/FastAPI deployment)
- **Database**: Supabase (already cloud-hosted)
- **File Storage**: Supabase Storage or AWS S3 (for ML models)

## 🎯 Prerequisites

Before deployment, ensure you have:
- ✅ Supabase project set up with all tables and RLS policies
- ✅ Google Earth Engine service account credentials
- ✅ Mapbox API token
- ✅ Polar.sh account for payments (optional)
- ✅ Git repository (GitHub, GitLab, or Bitbucket)

---

## 🌐 Frontend Deployment (Vercel)

### Why Vercel?
- Built by Next.js creators
- Automatic deployments from Git
- Edge network for fast global performance
- Zero configuration for Next.js
- Free generous tier

### Step 1: Prepare Frontend

```bash
cd frontend

# Ensure build works locally
npm run build

# Test production build
npm run start
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? terrafoma-frontend
# - Directory? ./
# - Override settings? No
```

#### Option B: Using Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub
2. **Click "Add New Project"**
3. **Import your Git repository**
4. **Configure:**
   - Framework Preset: `Next.js`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

### Step 3: Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

```env
# Backend API
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app

# Mapbox
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here

# Optional: Polar.sh
NEXT_PUBLIC_POLAR_CHECKOUT_URL=your_polar_checkout_url
```

### Step 4: Deploy

- Click **"Deploy"**
- Wait for build to complete (~2-3 minutes)
- Your frontend will be live at: `https://terrafoma-frontend.vercel.app`

### Custom Domain (Optional)

1. Go to **Settings → Domains**
2. Add your domain (e.g., `terrafoma.com`)
3. Follow DNS configuration instructions
4. SSL certificate auto-configured

---

## ⚙️ Backend Deployment (Railway)

### Why Railway?
- Simple Python/FastAPI deployment
- Automatic HTTPS
- Built-in monitoring
- PostgreSQL support (if needed)
- Free $5/month credit

### Step 1: Prepare Backend

```bash
cd backend

# Create requirements.txt if not exists
pip freeze > requirements.txt

# Create Procfile for Railway
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Create railway.json for configuration
cat > railway.json <<EOF
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
```

### Step 2: Deploy to Railway

#### Option A: Using Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up
```

#### Option B: Using Railway Dashboard (Recommended)

1. **Go to [railway.app](https://railway.app)** and sign in with GitHub
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Select your repository**
5. **Configure:**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables

In Railway Dashboard → Variables, add:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Google Earth Engine
GEE_SERVICE_ACCOUNT_EMAIL=your-service-account@project.iam.gserviceaccount.com
GEE_PRIVATE_KEY_PATH=/app/gee-credentials.json

# Optional: Direct GEE credentials as env var
GEE_CREDENTIALS={"type":"service_account","project_id":"..."}

# API Configuration
CORS_ORIGINS=["https://terrafoma-frontend.vercel.app","http://localhost:3001"]

# Python
PYTHONUNBUFFERED=1
```

### Step 4: Upload ML Model

**Option A: Include in Git (if < 100MB)**
```bash
# Add model to git
git lfs track "*.pkl"
git add backend/ml/models/biomass_model_v1.pkl
git commit -m "Add ML model"
git push
```

**Option B: Upload to Cloud Storage**
```bash
# Upload to Supabase Storage
# Or use AWS S3, Google Cloud Storage

# Modify biomass_estimator.py to download model on startup
```

### Step 5: Deploy

- Your backend will be live at: `https://your-app.railway.app`
- Update Vercel environment variable `NEXT_PUBLIC_API_URL` with this URL

---

## 🔄 Alternative: Backend on Render

### Why Render?
- Free tier available
- Automatic deployments
- Simple configuration
- Good Python support

### Deployment Steps

1. **Go to [render.com](https://render.com)** and sign in with GitHub
2. **Click "New +" → "Web Service"**
3. **Connect your repository**
4. **Configure:**
   - Name: `terrafoma-backend`
   - Region: Choose closest to your users
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables** (same as Railway)
6. **Select Plan**: Free or paid
7. **Create Web Service**

---

## 🎨 Alternative: All-in-One on Railway

Deploy both frontend and backend on Railway as a unified solution. This approach keeps everything in one place for easier management.

### Why All-in-One Railway?
- ✅ Unified billing and monitoring
- ✅ Single dashboard for both services
- ✅ Simplified environment variable management
- ✅ Automatic service discovery and networking
- ⚠️ Slightly more expensive than Vercel + Railway combo
- ⚠️ Frontend may not be as optimized as Vercel's edge network

### Step-by-Step Deployment

#### 1. Prepare Your Repository

Ensure your code is pushed to GitHub:
```bash
cd /Users/cococe/Desktop/terrafoma
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

#### 2. Deploy Backend Service

**Via Railway Dashboard:**

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your **terrafoma** repository
5. Railway will detect a monorepo - click **"Add variables"** first

**Configure Backend Service:**
- **Service Name**: `terrafoma-backend`
- **Root Directory**: `backend`
- **Build Command**: (Auto-detected) `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Add Environment Variables** (Settings → Variables):
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
GEE_SERVICE_ACCOUNT_EMAIL=your-gee-account@project.iam.gserviceaccount.com
GEE_PRIVATE_KEY_PATH=/app/gee-credentials.json
PYTHONUNBUFFERED=1
```

6. Click **"Deploy"** and wait for build to complete (~3-5 minutes)
7. Note your backend URL: `https://terrafoma-backend-production.up.railway.app`

#### 3. Deploy Frontend Service

**From the same Railway Project:**

1. In your Railway project dashboard, click **"+ New"** → **"Service"**
2. Select **"GitHub Repo"** → Choose the same repository
3. Click **"Add Service"**

**Configure Frontend Service:**
- **Service Name**: `terrafoma-frontend`
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run start`

**Set Environment Variables** (Settings → Variables):
```env
# Use the backend URL from step 2
NEXT_PUBLIC_API_URL=https://terrafoma-backend-production.up.railway.app
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
PORT=3000
NODE_ENV=production
```

4. Click **"Deploy"**
5. Wait for build (~2-3 minutes)
6. Your frontend URL: `https://terrafoma-frontend-production.up.railway.app`

#### 4. Configure Service Communication

**Update Backend CORS:**

Railway services can communicate via internal networking. Update your backend's allowed origins:

1. Go to Backend Service → **Variables**
2. Add or update:
```env
CORS_ORIGINS=["https://terrafoma-frontend-production.up.railway.app","http://localhost:3001"]
```

3. Redeploy backend (Settings → click **"Redeploy"**)

#### 5. Verify Deployment

**Test Backend:**
```bash
# Health check
curl https://terrafoma-backend-production.up.railway.app/health

# Open API docs
open https://terrafoma-backend-production.up.railway.app/docs
```

**Test Frontend:**
```bash
# Open in browser
open https://terrafoma-frontend-production.up.railway.app

# Check if API connection works (check browser console)
```

**Test Full Flow:**
1. Register a new user
2. Login as admin
3. Scan a land plot
4. Check if landowner receives notification
5. Browse marketplace

#### 6. Set Up Custom Domains (Optional)

**Both services can have custom domains:**

**Backend:**
1. Backend Service → Settings → **Domains**
2. Click **"Generate Domain"** or **"Custom Domain"**
3. For custom: Add your domain (e.g., `api.terrafoma.com`)
4. Configure DNS with provided CNAME records

**Frontend:**
1. Frontend Service → Settings → **Domains**
2. Click **"Generate Domain"** or **"Custom Domain"**
3. For custom: Add your domain (e.g., `app.terrafoma.com` or `terrafoma.com`)
4. Configure DNS with provided CNAME records

**Update environment variables after setting custom domains:**
- Frontend: Update `NEXT_PUBLIC_API_URL` to your API domain
- Backend: Update `CORS_ORIGINS` to include your frontend domain

#### 7. Monitoring and Logs

**View Logs:**
- Click on any service → **Deployments** tab
- Click on latest deployment → **View Logs**
- Real-time logs stream automatically

**Monitor Resources:**
- Each service shows CPU, Memory, and Network usage
- Set up usage alerts in **Settings → Usage Limits**

**Health Checks:**
Railway automatically monitors service health. Configure custom checks:
- Service → Settings → **Health Check**
- Path: `/health` (backend) or `/` (frontend)
- Interval: 60 seconds

#### 8. Cost Management

**Railway Pricing:**
- $5/month free credit for hobby plan
- Usage-based pricing after free credit:
  - ~$0.000463 per GB-hour for memory
  - ~$0.000231 per vCPU-hour for CPU
  - Free egress up to 100GB

**Estimated Monthly Cost for Both Services:**
- Light usage (MVP/Demo): $5-10/month
- Medium traffic: $15-25/month
- Production with moderate traffic: $30-50/month

**Cost Optimization Tips:**
1. Use **sleep mode** for frontend in hobby projects (auto-wake on request)
2. Set **memory limits** to prevent overages (512MB frontend, 1GB backend)
3. Enable **auto-scaling** only if needed
4. Monitor usage in **Project → Usage** tab

#### 9. Update and Redeploy

**Automatic Deployments:**
Railway automatically redeploys on git push to main branch:
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
# Both services will auto-deploy
```

**Manual Redeployment:**
- Go to service → Deployments → Click **"Redeploy"** on any previous deployment
- Or trigger from GitHub Actions

**Rollback:**
- Go to Deployments tab
- Find previous working deployment
- Click **"Redeploy"** on that deployment

#### 10. Environment-Specific Configurations

**Create different environments:**

1. **Development Environment:**
   - Create a new Railway project: "terrafoma-dev"
   - Deploy from `dev` branch
   - Use separate Supabase project

2. **Staging Environment:**
   - Create another project: "terrafoma-staging"
   - Deploy from `staging` branch
   - Use staging Supabase instance

3. **Production Environment:**
   - Deploy from `main` branch
   - Use production Supabase with backups

### Alternative: Using Railway CLI

**Install Railway CLI:**
```bash
npm i -g @railway/cli
railway login
```

**Initialize Project:**
```bash
cd /Users/cococe/Desktop/terrafoma
railway init
# Select: Create new project
# Name: terrafoma
```

**Deploy Backend:**
```bash
cd backend
railway up
# Railway detects Python and deploys automatically
```

**Deploy Frontend:**
```bash
cd ../frontend
railway service create
railway up
```

**Link Services:**
```bash
# Railway automatically handles service discovery
# Use public URLs or internal networking
```

### Troubleshooting All-in-One Railway

**Build Failures:**
```bash
# Backend: Missing dependencies
# Fix: Ensure all packages in requirements.txt
cd backend && pip freeze > requirements.txt

# Frontend: Node version mismatch
# Add .nvmrc file to frontend:
echo "18" > frontend/.nvmrc
```

**Port Binding Issues:**
```bash
# Ensure your apps bind to $PORT environment variable
# Backend: Already using $PORT in Procfile ✓
# Frontend: Next.js automatically uses $PORT ✓
```

**Environment Variables Not Loading:**
```bash
# Check in Railway Dashboard → Service → Variables
# Ensure no typos in variable names
# Redeploy after adding new variables
```

**ML Model Not Found:**
```bash
# Check model file size
ls -lh backend/ml/models/biomass_model_v1.pkl

# If > 100MB, use Git LFS or cloud storage:
# 1. Upload to Supabase Storage
# 2. Download on app startup
```

**Service Can't Communicate:**
```bash
# Use public URLs, not internal Railway networking
# Frontend should use: NEXT_PUBLIC_API_URL=https://backend.railway.app
# Not: NEXT_PUBLIC_API_URL=backend.railway.internal
```

### Comparison: Vercel+Railway vs All-Railway

| Feature | Vercel + Railway | All Railway |
|---------|------------------|-------------|
| **Cost** | $0-5/month | $10-20/month |
| **Setup Time** | 10 minutes | 15 minutes |
| **Frontend Performance** | ⭐⭐⭐⭐⭐ (Edge network) | ⭐⭐⭐⭐ (Good) |
| **Management** | Two dashboards | One dashboard |
| **Scaling** | Auto (Vercel) | Manual config |
| **Learning Curve** | Easy | Easy |
| **Recommended For** | Production | Development/Testing |

### Final Checklist

- [ ] Both services deployed successfully
- [ ] Backend URL saved and configured in frontend
- [ ] All environment variables set correctly
- [ ] CORS configured with frontend URL
- [ ] Custom domains configured (optional)
- [ ] Health checks passing
- [ ] Logs reviewed for errors
- [ ] Test all critical user flows
- [ ] Monitoring and alerts set up
- [ ] Backup and rollback plan documented

---

## 📦 Database & Storage

### Supabase (Already Set Up)
- ✅ No deployment needed
- ✅ Already cloud-hosted
- ✅ Global CDN
- ✅ Automatic backups

### Verify Production Settings:
```sql
-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Verify admin bypass works
-- Test with service role key
```

---

## 🔧 Post-Deployment Configuration

### 1. Update CORS Origins

In `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://terrafoma-frontend.vercel.app",
        "https://terrafoma.com",  # Your custom domain
        "http://localhost:3001",  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Update Frontend API URL

In `frontend/src/lib/api.ts`:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';
```

### 3. Configure Supabase Auth Redirects

In Supabase Dashboard → Authentication → URL Configuration:
- Site URL: `https://terrafoma-frontend.vercel.app`
- Redirect URLs: Add your production URLs

### 4. Update Mapbox Allowed URLs

In Mapbox Dashboard → Account → Tokens:
- Add `https://terrafoma-frontend.vercel.app` to allowed URLs

---

## 🔐 Security Checklist

- [ ] All environment variables set correctly
- [ ] Supabase RLS policies enabled
- [ ] Service role key only used in backend (never exposed to frontend)
- [ ] CORS configured with specific origins (no wildcards in production)
- [ ] API rate limiting configured
- [ ] HTTPS enabled (automatic with Vercel/Railway)
- [ ] Secrets not committed to Git
- [ ] Google Earth Engine service account has minimal permissions

---

## 📊 Monitoring & Logs

### Vercel
- Dashboard → Your Project → Deployments → View Logs
- Real-time logs for each deployment
- Performance analytics included

### Railway
- Dashboard → Your Service → Logs
- Metrics for CPU, Memory, Network
- Set up alerts for errors

### Render
- Dashboard → Your Service → Logs
- Metrics dashboard
- Health checks

---

## 🧪 Testing Production

### 1. Test API Endpoints
```bash
# Health check
curl https://your-backend.railway.app/health

# API docs
open https://your-backend.railway.app/docs

# Test auth
curl https://your-backend.railway.app/api/auth/test
```

### 2. Test Frontend
```bash
# Open in browser
open https://terrafoma-frontend.vercel.app

# Test critical flows:
# - User registration
# - Login/logout
# - Land registration
# - Admin scan
# - Marketplace
```

### 3. Monitor Errors
- Check Vercel logs for frontend errors
- Check Railway logs for backend errors
- Monitor Supabase logs for database issues

---

## 🚨 Troubleshooting

### Frontend Not Loading
```bash
# Check build logs in Vercel
# Common issues:
# - Missing environment variables
# - TypeScript errors
# - API URL incorrect

# Fix: Redeploy with correct env vars
vercel --prod
```

### Backend Not Starting
```bash
# Check Railway logs
# Common issues:
# - Missing dependencies in requirements.txt
# - Python version mismatch
# - Port binding issues

# Fix: Ensure Procfile uses $PORT
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### CORS Errors
```bash
# Check browser console
# Fix: Add frontend URL to CORS_ORIGINS in backend
```

### Database Connection Failed
```bash
# Verify Supabase credentials
# Check if service role key is correct
# Ensure database is accessible from Railway/Render IP
```

### ML Model Not Found
```bash
# Check if model file is included in deployment
# Option 1: Use Git LFS
# Option 2: Download from cloud storage on startup
```

---

## 💰 Cost Estimates

### Free Tier (Suitable for MVP/Demo)
- **Vercel**: Free (100GB bandwidth, unlimited requests)
- **Railway**: $5/month credit (enough for light usage)
- **Render**: Free tier (sleeps after 15min inactivity)
- **Supabase**: Free (500MB database, 1GB storage)
- **Total**: $0-5/month

### Production Tier (Suitable for Launch)
- **Vercel Pro**: $20/month (better performance, no team limit)
- **Railway**: ~$10-20/month (based on usage)
- **Supabase Pro**: $25/month (8GB database, 100GB storage)
- **Total**: ~$55-65/month

---

## 🔄 CI/CD Pipeline

### Automatic Deployments

Both Vercel and Railway support automatic deployments:

1. **Push to `main` branch** → Automatic production deployment
2. **Create PR** → Preview deployment with unique URL
3. **Merge PR** → Production deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: backend
```

---

## 📚 Additional Resources

### Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Supabase Docs](https://supabase.com/docs)

### Community
- [Vercel Discord](https://vercel.com/discord)
- [Railway Discord](https://discord.gg/railway)
- [Supabase Discord](https://discord.supabase.com)

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Code pushed to Git repository
- [ ] All tests passing locally
- [ ] Environment variables documented
- [ ] Database migrations applied
- [ ] ML model accessible

### Frontend Deployment
- [ ] Vercel project created
- [ ] Repository connected
- [ ] Environment variables set
- [ ] Build successful
- [ ] Custom domain configured (optional)

### Backend Deployment
- [ ] Railway/Render project created
- [ ] Repository connected
- [ ] Environment variables set
- [ ] ML model uploaded/accessible
- [ ] Health check passing

### Post-Deployment
- [ ] Frontend loads correctly
- [ ] API endpoints responding
- [ ] Database connections working
- [ ] Authentication functional
- [ ] File uploads working
- [ ] ML predictions working
- [ ] Monitoring set up
- [ ] Error tracking configured

---

## 🎉 You're Live!

Once deployed, your TerraFoma platform will be accessible globally:

- **Frontend**: `https://terrafoma-frontend.vercel.app`
- **Backend**: `https://terrafoma-backend.railway.app`
- **API Docs**: `https://terrafoma-backend.railway.app/docs`

**Next Steps:**
1. Set up monitoring and alerts
2. Configure custom domain
3. Enable analytics
4. Set up error tracking (Sentry)
5. Implement CI/CD pipeline
6. Plan scaling strategy

Good luck with your launch! 🚀🌍

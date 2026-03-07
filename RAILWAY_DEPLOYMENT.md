# 🚂 Railway All-in-One Deployment - Quick Guide

## TL;DR - Deploy in 15 Minutes

### Prerequisites
- ✅ Code pushed to GitHub
- ✅ Supabase project ready
- ✅ Railway account (sign up at railway.app)

---

## Step 1: Deploy Backend (5 minutes)

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
2. Select your **terrafoma** repository
3. Configure:
   ```
   Service Name: terrafoma-backend
   Root Directory: backend
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Add variables:
   ```env
   SUPABASE_URL=https://xyz.supabase.co
   SUPABASE_ANON_KEY=your_key
   SUPABASE_SERVICE_ROLE_KEY=your_service_key
   GEE_SERVICE_ACCOUNT_EMAIL=your-gee@project.iam.gserviceaccount.com
   PYTHONUNBUFFERED=1
   ```
5. Click **Deploy**
6. **Save your backend URL**: `https://terrafoma-backend-xxx.up.railway.app`

---

## Step 2: Deploy Frontend (5 minutes)

1. In same Railway project → **+ New** → **Service** → **GitHub Repo**
2. Select same repository
3. Configure:
   ```
   Service Name: terrafoma-frontend
   Root Directory: frontend
   Build: npm install && npm run build
   Start: npm run start
   ```
4. Add variables:
   ```env
   NEXT_PUBLIC_API_URL=https://terrafoma-backend-xxx.up.railway.app
   NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
   PORT=3000
   NODE_ENV=production
   ```
5. Click **Deploy**
6. **Save your frontend URL**: `https://terrafoma-frontend-xxx.up.railway.app`

---

## Step 3: Update CORS (2 minutes)

1. Go to **Backend Service** → **Variables**
2. Add:
   ```env
   CORS_ORIGINS=["https://terrafoma-frontend-xxx.up.railway.app","http://localhost:3001"]
   ```
3. Click **Redeploy**

---

## Step 4: Test (3 minutes)

### Backend Test
```bash
curl https://your-backend-url.up.railway.app/health
# Should return: {"status": "healthy"}

# View API docs
open https://your-backend-url.up.railway.app/docs
```

### Frontend Test
```bash
open https://your-frontend-url.up.railway.app
```

### Full Flow Test
1. ✅ Register new user
2. ✅ Login as admin
3. ✅ Scan land plot
4. ✅ Check landowner notifications
5. ✅ Browse marketplace

---

## Common Issues & Fixes

### Build Failed - Backend
```bash
# Missing dependencies
cd backend
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Build Failed - Frontend
```bash
# Node version issue - add .nvmrc
echo "18" > frontend/.nvmrc
git add frontend/.nvmrc
git commit -m "Set Node version"
git push

# Security vulnerabilities - update dependencies
cd frontend
npm update next@latest
npm audit fix
git add package.json package-lock.json
git commit -m "Fix: Update dependencies for security"
git push
```

### CORS Errors
```bash
# Ensure backend CORS_ORIGINS includes frontend URL
# Format: ["https://frontend.railway.app"]
# NOT: https://frontend.railway.app (no quotes)
```

### 502 Bad Gateway
```bash
# Backend not starting - check logs
# Railway Dashboard → Backend → Deployments → View Logs
# Common issues:
# - Port binding (use $PORT variable)
# - Missing environment variables
# - Python package conflicts
```

### Frontend Can't Reach Backend
```bash
# Check environment variable
# Railway Dashboard → Frontend → Variables
# NEXT_PUBLIC_API_URL must match backend URL exactly
# Include https://, no trailing slash
```

### ML Model Not Loading
```bash
# Check if model file is in git
ls -lh backend/ml/models/biomass_model_v1.pkl

# If too large (>100MB), use Git LFS:
git lfs track "*.pkl"
git add .gitattributes
git add backend/ml/models/biomass_model_v1.pkl
git commit -m "Add ML model with LFS"
git push
```

---

## View Logs

### Real-time Logs
```bash
# Install Railway CLI
npm i -g @railway/cli
railway login

# View backend logs
railway logs -s terrafoma-backend

# View frontend logs
railway logs -s terrafoma-frontend
```

### Dashboard Logs
- Railway Dashboard → Service → **Deployments**
- Click latest deployment → **View Logs**
- Logs stream in real-time

---

## Update Deployment

### Automatic (Recommended)
```bash
# Any push to main branch auto-deploys
git add .
git commit -m "Update features"
git push origin main
# Wait 2-3 minutes for deployment
```

### Manual Redeploy
1. Railway Dashboard → Service → **Deployments**
2. Click **⋮** on any deployment
3. Click **Redeploy**

---

## Rollback

If something breaks:
1. Railway Dashboard → Service → **Deployments**
2. Find last working deployment
3. Click **⋮** → **Redeploy**

---

## Cost Estimate

### Free Tier
- $5/month credit included
- Enough for development/testing
- ~500MB RAM per service
- ~1GB total combined

### Light Production
- $10-15/month
- Good for MVP with <1000 users
- 512MB frontend + 1GB backend

### Medium Production
- $20-30/month
- 10,000+ requests/day
- 1GB frontend + 2GB backend

### Monitor Usage
Railway Dashboard → Project → **Usage** tab

---

## Pro Tips

### Cost Optimization
```bash
# Set memory limits to avoid overages
Railway Dashboard → Service → Settings → Memory Limit
Frontend: 512MB
Backend: 1GB
```

### Custom Domains
```bash
# Free Railway domain (included)
Service → Settings → Domains → Generate Domain

# Custom domain (you own)
Service → Settings → Domains → Custom Domain
Add your domain → Configure DNS
```

### Environment Variables
```bash
# Use Railway CLI for bulk updates
railway variables set KEY1=value1 KEY2=value2 KEY3=value3
```

### Service Templates
```bash
# Save time on next deployment
Railway Dashboard → Project → Settings → Template
Create template from current setup
```

### Monitoring
```bash
# Set up health checks
Service → Settings → Health Check
Path: /health
Interval: 60s
Timeout: 30s
```

---

## Quick Commands Reference

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Open service in browser
railway open

# Set variables
railway variables set KEY=value

# Deploy
railway up

# Check status
railway status

# View environment
railway environment
```

---

## Need Help?

### Documentation
- Full Guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

### Troubleshooting Checklist
- [ ] Both services showing "Active" status
- [ ] Environment variables set correctly (no typos)
- [ ] Backend URL in frontend env vars
- [ ] Frontend URL in backend CORS
- [ ] ML model file accessible
- [ ] Supabase credentials correct
- [ ] GEE credentials configured
- [ ] Logs show no errors

---

## Success! 🎉

Your TerraFoma platform is now live:
- **Frontend**: `https://terrafoma-frontend-xxx.up.railway.app`
- **Backend**: `https://terrafoma-backend-xxx.up.railway.app`
- **API Docs**: `https://terrafoma-backend-xxx.up.railway.app/docs`

Share your platform and start connecting landowners with carbon markets! 🌍💚

# Railway Deployment Setup Guide

## Critical Environment Variables Required

### Frontend Service Variables

**MUST be set in Railway Dashboard → Frontend Service → Variables tab:**

```bash
# Mapbox (CRITICAL - Map won't work without this)
# Get your token from: https://account.mapbox.com/access-tokens/
NEXT_PUBLIC_MAPBOX_TOKEN=pk.your_mapbox_token_here

# Backend API URL (Replace with your actual backend Railway URL)
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app

# Polar Payment Integration
POLAR_SERVER=sandbox
POLAR_ACCESS_TOKEN=your_polar_access_token
POLAR_PRODUCT_ID=your_polar_product_id
POLAR_WEBHOOK_SECRET=your_polar_webhook_secret
```

## How to Set Environment Variables in Railway

### Method 1: Railway Dashboard (Recommended)
1. Go to https://railway.app/dashboard
2. Select your project
3. Click on **Frontend Service**
4. Click **Variables** tab (left sidebar)
5. Click **+ New Variable**
6. For each variable:
   - Enter variable name (e.g., `NEXT_PUBLIC_MAPBOX_TOKEN`)
   - Enter value (e.g., `pk.eyJ1Ijo...`)
   - Click **Add**
7. Railway will automatically redeploy

### Method 2: Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Set variables
railway variables set NEXT_PUBLIC_MAPBOX_TOKEN="YOUR_MAPBOX_TOKEN_HERE"
railway variables set NEXT_PUBLIC_API_URL="https://your-backend.railway.app"
railway variables set POLAR_SERVER="sandbox"
railway variables set POLAR_ACCESS_TOKEN="YOUR_POLAR_TOKEN"
railway variables set POLAR_PRODUCT_ID="YOUR_POLAR_PRODUCT_ID"
railway variables set POLAR_WEBHOOK_SECRET="YOUR_POLAR_WEBHOOK_SECRET"

# Redeploy
railway up
```

## Service Configuration

### Frontend Service Settings:
- **Root Directory**: `frontend`
- **Builder**: Dockerfile (from railway.json)
- **Start Command**: `node server.js` (from railway.json)

### Backend Service Settings:
- **Root Directory**: `backend`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Debugging Checklist

After deployment, check Railway logs:

### ✅ Expected Log Output (Server-side - Railway Logs):
```
=== CONFIG API DEBUG ===
NEXT_PUBLIC_MAPBOX_TOKEN exists: true
Token length: 110
Token preview: pk.eyJ1IjoibWFu...
NODE_ENV: production
========================
```

### ❌ Problem Indicators (Server-side):
```
NEXT_PUBLIC_MAPBOX_TOKEN exists: false
Token length: 0
Token preview: EMPTY
❌ CRITICAL: Mapbox token not found in environment variables!
```

### Browser Console (Client-side):
After deployment completes, open your Railway frontend URL and check browser console:

**✅ Success:**
```
=== CLIENT CONFIG DEBUG ===
Full config response: { mapboxToken: "pk.eyJ...", debug: { hasToken: true, tokenLength: 110 } }
Token length: 110
✓ Mapbox token set successfully
```

**❌ Problem:**
```
=== CLIENT CONFIG DEBUG ===
Full config response: { mapboxToken: "", debug: { hasToken: false, tokenLength: 0 } }
Token length: 0
❌ Mapbox token not configured - token is empty or undefined
```

## Common Issues & Solutions

### Issue 1: "Mapbox token not configured"
**Cause**: `NEXT_PUBLIC_MAPBOX_TOKEN` not set in Railway
**Solution**: Add the variable in Railway dashboard → redeploy

### Issue 2: Map still not showing after setting variable
**Cause**: Need to redeploy after adding variables
**Solution**: 
- Push a new commit: `git commit --allow-empty -m "Redeploy" && git push`
- Or click "Redeploy" in Railway dashboard

### Issue 3: "package.json not found"
**Cause**: Root directory not set correctly
**Solution**: Set Root Directory to `frontend` in Service Settings

### Issue 4: Build runs out of memory
**Cause**: Next.js build needs more memory
**Solution**: Already configured in Dockerfile with `--max-old-space-size=4096`

## Verification Steps

1. **Check Variables are Set:**
   ```bash
   railway variables
   ```

2. **Check Deployment Logs:**
   - Railway Dashboard → Deployments → View Logs
   - Look for "=== CONFIG API DEBUG ===" output

3. **Test in Browser:**
   - Open deployed URL
   - Open DevTools (F12) → Console
   - Look for debug output
   - Navigate to /scan page
   - Map should load

4. **Test API Endpoint:**
   ```bash
   curl https://your-frontend.railway.app/api/config
   ```
   Should return:
   ```json
   {
     "mapboxToken": "pk.eyJ1...",
     "debug": {
       "hasToken": true,
       "tokenLength": 110,
       "environment": "production",
       "railway": true
     }
   }
   ```

## Contact

If issues persist, check:
- Railway service logs (server-side)
- Browser console (client-side)
- Both should now have detailed debug output

Admin email: mangamhizha@gmail.com

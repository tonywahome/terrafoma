# Fix Railway Frontend Deployment Crashes

## Problem
Frontend keeps crashing with "Killed" error during build. This happens because:
1. Next.js build process uses too much memory (default 512MB-1GB on Railway)
2. Missing `sharp` package for image optimization
3. Large dependencies (mapbox, recharts) consuming memory

## ✅ Changes Made

### 1. **Increased Build Memory**
- `package.json`: Added `NODE_OPTIONS='--max-old-space-size=4096'` to build script (4GB memory limit)
- `railway.json`: Added explicit buildCommand with memory optimization
- `nixpacks.toml`: Added Nixpacks configuration with 4GB memory

### 2. **Added Sharp Package**
- `package.json`: Added `"sharp": "^0.33.5"` for production image optimization
- This prevents Next.js warnings and improves performance

### 3. **Optimized Next.js Config**
- `next.config.js`:
  - Added `output: 'standalone'` for smaller Docker images
  - Added webpack optimizations to reduce bundle size
  - Added experimental package import optimization
  - Added image remote patterns

### 4. **Created Dockerfile Alternative**
- `frontend/Dockerfile`: Multi-stage Docker build as backup if Nixpacks fails

## 🚀 Deploy to Railway

### Option 1: Use Updated Nixpacks (Recommended)

1. **Install sharp locally first:**
   ```bash
   cd frontend
   npm install sharp
   ```

2. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Fix Railway deployment crashes - increase build memory and add sharp"
   git push
   ```

3. **Railway will automatically rebuild** with new configuration

### Option 2: Use Docker Build (If Nixpacks Still Fails)

1. In Railway dashboard → Your Frontend Service → Settings:
   - Scroll to "Build Method"
   - Change from "Nixpacks" to **"Dockerfile"**
   - Set Dockerfile path: `frontend/Dockerfile`

2. Push changes:
   ```bash
   git add .
   git commit -m "Switch to Docker build for Railway"
   git push
   ```

### Option 3: Increase Railway Memory (If Available)

1. In Railway dashboard → Your Frontend Service → Settings:
   - Scroll to "Resources"
   - Increase memory allocation to **2GB or 4GB**
   - This requires a paid plan

## 🔍 Monitor Build Progress

1. Go to Railway dashboard
2. Click on your frontend service
3. Watch the "Deployments" tab
4. Check logs for:
   ```
   ✓ Creating an optimized production build
   ✓ Compiled successfully
   ```

## ⚠️ Common Issues

### Issue: Still getting "Killed"
**Solution:** 
- Upgrade Railway plan for more memory
- Use Option 2 (Dockerfile)
- Check if you're on Railway's free tier (limited to 512MB)

### Issue: "Cannot find module 'sharp'"
**Solution:**
```bash
cd frontend
npm install
git add package-lock.json
git commit -m "Update package-lock with sharp"
git push
```

### Issue: Build succeeds but deployment fails
**Solution:** Check Railway environment variables:
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
PORT=3000
NODE_ENV=production
```

## 📊 Expected Build Output

Successful build should show:
```
Route (app)                                Size
┌ ○ /                                     XX kB
├ ○ /dashboard                            XX kB
├ ○ /marketplace                          XX kB
├ ○ /scan                                 XX kB
└ ○ /landowner/pending-scans             XX kB

○ (Static)  prerendered as static content
ƒ (Dynamic) server-rendered on demand
```

## 🎯 Test After Deployment

1. Visit: https://terrafoma-production.up.railway.app
2. Check homepage loads
3. Try login/signup
4. Navigate to different pages

## 💡 Alternative: Deploy to Vercel Instead

If Railway continues to have issues:
```bash
npm install -g vercel
cd frontend
vercel --prod
```

Vercel has better Next.js optimization and won't have memory issues.

## 📝 Files Modified

- ✅ `frontend/package.json` - Added sharp, increased build memory
- ✅ `frontend/railway.json` - Added buildCommand with memory optimization
- ✅ `frontend/nixpacks.toml` - Configured Nixpacks build
- ✅ `frontend/next.config.js` - Added production optimizations
- ✅ `frontend/Dockerfile` - Created Docker alternative

## ✅ Next Steps

1. Run `npm install` in frontend folder
2. Commit all changes
3. Push to trigger Railway deployment
4. Monitor deployment logs
5. Test the live site

Good luck! 🚀

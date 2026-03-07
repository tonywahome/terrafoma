# 🚀 Quick Deployment Commands

## Pre-Deployment Check
```bash
./deploy-check.sh
```

## Deploy Frontend to Vercel

### One-Command Deploy
```bash
cd frontend
npx vercel --prod
```

### First-Time Setup
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Production deployment
vercel --prod
```

## Deploy Backend to Railway

### Using Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project (first time)
cd backend
railway link

# Deploy
railway up
```

### Using Git Push (after initial setup)
```bash
git add .
git commit -m "Deploy updates"
git push origin main
# Railway auto-deploys from GitHub
```

## Deploy Backend to Render

### Using Dashboard
1. Go to render.com
2. New → Web Service
3. Connect repository
4. Configure settings
5. Deploy

## Environment Variables

### Frontend (Vercel)
```bash
vercel env add NEXT_PUBLIC_API_URL
vercel env add NEXT_PUBLIC_MAPBOX_TOKEN
```

### Backend (Railway)
```bash
railway variables set SUPABASE_URL=your_url
railway variables set SUPABASE_ANON_KEY=your_key
railway variables set SUPABASE_SERVICE_ROLE_KEY=your_service_key
```

## Update Production

### Frontend
```bash
cd frontend
git pull
npm install
vercel --prod
```

### Backend
```bash
cd backend
git pull
railway up
# or just: git push origin main (if auto-deploy enabled)
```

## Rollback

### Vercel
```bash
# Go to dashboard → Deployments
# Click on previous deployment → "Promote to Production"
```

### Railway
```bash
railway rollback
```

## Health Checks

### Backend
```bash
curl https://your-backend.railway.app/health
curl https://your-backend.railway.app/docs
```

### Frontend
```bash
curl https://your-frontend.vercel.app
```

## View Logs

### Vercel
```bash
vercel logs
```

### Railway
```bash
railway logs
```

## Quick Links

After deployment, save these URLs:

- Frontend: https://__________.vercel.app
- Backend: https://__________.railway.app
- API Docs: https://__________.railway.app/docs
- Supabase Dashboard: https://app.supabase.com

## Emergency Rollback

If production breaks:

1. **Frontend**: Vercel dashboard → Previous deployment → Promote
2. **Backend**: Railway dashboard → Previous deployment → Redeploy
3. **Database**: Supabase dashboard → Database → Point-in-time recovery

## Support

- Full guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Vercel docs: https://vercel.com/docs
- Railway docs: https://docs.railway.app

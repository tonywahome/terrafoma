# TerraFoma — Deployment Guide

- **Backend (FastAPI)** → [Render](https://render.com)
- **Frontend (Next.js)** → [Vercel](https://vercel.com)

---

## Step 1 — Deploy the Backend on Render

1. Push this repo to GitHub (if not already done).
2. Go to [render.com](https://render.com) → **New** → **Web Service**.
3. Connect your GitHub account and select this repository.
4. Configure the service:
   - **Root Directory**: `backend`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add **Environment Variables**:

| Variable | Value |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | Your Supabase anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | Your Supabase service role key |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app,http://localhost:3000` |

6. Click **Deploy**. Note the service URL (e.g., `https://terrafoma-api.onrender.com`).

> Alternatively, use **Render Blueprint**: go to **New → Blueprint** and select the repo — it will auto-configure the service from the `render.yaml` in the repo root.

---

## Step 2 — Deploy the Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project** → import this repo.
2. **Set Root Directory to `frontend`**.
3. Framework Preset: **Next.js** (auto-detected).
4. Add **Environment Variables**:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | The Render backend URL from Step 1 (e.g., `https://terrafoma-api.onrender.com`) |
| `NEXT_PUBLIC_MAPBOX_TOKEN` | Your Mapbox public token |
| `POLAR_SERVER` | `sandbox` (or `production` when going live) |
| `POLAR_ACCESS_TOKEN` | Your Polar access token |
| `POLAR_PRODUCT_ID` | Your Polar product ID |
| `POLAR_WEBHOOK_SECRET` | Your Polar webhook secret |
| `POLAR_SUCCESS_URL` | `https://your-frontend.vercel.app/purchase-success?checkout_id={CHECKOUT_ID}` |

5. Click **Deploy**.

> `NEXT_PUBLIC_*` variables are baked in at build time — changing them in the dashboard requires a redeploy to take effect.

---

## Step 3 — Post-Deployment

### Update CORS
After the frontend is deployed, go back to the **Render** backend service:

- **Environment** tab → update `CORS_ORIGINS` to include the real frontend URL.
- Render auto-redeploys on env var save (or click **Manual Deploy**).

### Update Polar Success URL
In the **Vercel** frontend project:

- Update `POLAR_SUCCESS_URL` to use the real frontend domain instead of a placeholder.
- Redeploy.

### Database

- The backend uses Supabase when credentials are provided. Run `backend/data/schema.sql` in the Supabase SQL Editor to set up the schema.
- Without Supabase credentials, the backend falls back to an **in-memory database** which resets on every restart — not suitable for production.

---

## Notes

- **CORS for Vercel previews**: The backend's `allow_origin_regex` already permits all `*.vercel.app` subdomains, so frontend preview deployments work without extra CORS config.
- **ML models**: The satellite scan feature falls back to formula-based estimation since model `.pkl` files are not committed to the repo.
- **Cold starts**: Render free tier services spin down after 15 minutes of inactivity — the first request after inactivity can take ~30s. Upgrade to a paid instance type (`starter` or above) to keep the service always-on.

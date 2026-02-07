# Deploy Kiosk Web App on Vercel

This folder is a Vite + React app ready to deploy on [Vercel](https://vercel.com).

## Steps

1. **Push this repo to GitHub** (if not already).

2. **Import on Vercel**
   - Go to [vercel.com](https://vercel.com) → **Add New** → **Project**.
   - Import your Git repository.
   - Set **Root Directory** to: `client-apps/kiosk-app/ui`
   - Click **Edit** next to Root Directory and enter that path, then **Continue**.

3. **Environment variable**
   - In **Environment Variables**, add:
     - **Name:** `VITE_API_URL`
     - **Value:** Your backend API URL (e.g. `https://your-backend.railway.app` or your own domain).
   - The frontend uses this to call the kiosk session/cart/history APIs.

4. **Deploy**
   - Click **Deploy**. Vercel will run `npm install` and `npm run build` and serve the `dist` output.

## Notes

- The **backend** (kiosk API) must be deployed elsewhere (e.g. Railway, Render, Fly.io) and must allow CORS from your Vercel domain.
- After deployment, set `VITE_API_URL` in Vercel to that backend URL and redeploy if you change it.

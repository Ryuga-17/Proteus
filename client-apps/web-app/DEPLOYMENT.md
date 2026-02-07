# Frontend Deployment Guide

This guide will help you deploy the Proteus web app (this folder: `client-apps/web-app`) to Vercel or other platforms.

## Prerequisites

1. **Build the project locally first** to ensure everything works:
   ```bash
   cd client-apps/web-app
   npm install
   npm run build
   ```

2. **Set up environment variables** for production (see below).

## Environment Variables

Create a `.env.production` file in this directory, or set in Vercel/Netlify:

```env
VITE_API_URL=https://your-backend-api-url.com
```

Optional (for virtual try-on / recommendations):
- `VITE_IMGBB_API_KEY` – ImgBB for image uploads
- `VITE_FAL_API_KEY` – FAL API for try-on
- `VITE_HUGGINGFACE_API_KEY` – Hugging Face API

**Important:** Replace `https://your-backend-api-url.com` with your actual backend API URL.

## Deploy to Vercel (recommended)

### Option A: Deploy script (one command)

From the repo root:

```bash
cd client-apps/web-app
chmod +x deploy.sh
./deploy.sh
```

Or manually:

```bash
cd client-apps/web-app
npm run build
npx vercel --prebuilt --yes
```

**First time:** Run `npx vercel login` in a terminal, complete the browser login, then run the script again.  
**Production:** Use `npx vercel --prebuilt --prod --yes` to deploy to the production URL.

### Option B: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) → Sign up or log in.
2. **Add New** → **Project** → Import your Git repository.
3. Set **Root Directory** to: `client-apps/web-app` (click Edit and enter that path).
4. **Environment Variables** (optional but recommended):
   - `VITE_API_URL` = your backend API URL (e.g. `https://your-api.railway.app` or similar).
5. Click **Deploy**. Vercel will run `npm install` and `npm run build` and serve the `dist` folder.

Build settings are already in `vercel.json` (build command, output directory, SPA rewrites).

### If you get 404 after deploy

1. **Check Root Directory**  
   In Vercel: Project → **Settings** → **General** → **Root Directory**.  
   It must be **`client-apps/web-app`** (no leading slash). If it’s empty or wrong, set it, save, then **Redeploy** (Deployments → ⋮ → Redeploy).

2. **Check build**  
   In Vercel: **Deployments** → open the latest deployment → **Building** tab.  
   Build must finish successfully and the output must be the `dist` folder from this app.

3. **Redeploy**  
   After fixing Root Directory, trigger a new deploy (push a commit or use **Redeploy**).

## Other deployment options

### Netlify

### Option 2: Netlify

1. **Install Netlify CLI** (optional):
   ```bash
   npm i -g netlify-cli
   ```

2. **Deploy**:
   ```bash
   cd client-apps/web-app
   netlify deploy --prod
   ```

3. **Or use Netlify Dashboard**:
   - Go to [netlify.com](https://netlify.com)
   - Sign up/login
   - Click "Add new site" → "Import an existing project"
   - Connect your Git repository
   - Set:
     - Base directory: `client-apps/web-app`
     - Build command: `npm run build`
     - Publish directory: `dist`
   - Add Environment Variable:
     - Key: `VITE_API_URL`
     - Value: `https://your-backend-api-url.com`
   - Click "Deploy site"

### Option 3: GitHub Pages

1. **Install gh-pages**:
   ```bash
   cd client-apps/web-app
   npm install --save-dev gh-pages
   ```

2. **Update package.json**:
   Add to `scripts`:
   ```json
   "predeploy": "npm run build",
   "deploy": "gh-pages -d dist"
   ```

3. **Update vite.config.ts**:
   ```typescript
   export default defineConfig({
     plugins: [react(), tailwindcss()],
     resolve: {
       alias: {
         "@": path.resolve(__dirname, "./src"),
       },
     },
     base: '/your-repo-name/', // Replace with your GitHub repo name
   });
   ```

4. **Deploy**:
   ```bash
   npm run deploy
   ```

### Option 4: Render

1. Go to [render.com](https://render.com)
2. Sign up/login
3. Click "New" → "Static Site"
4. Connect your Git repository
5. Configure:
   - Name: `proteus-frontend`
   - Root Directory: `client-apps/web-app`
   - Build Command: `npm run build`
   - Publish Directory: `dist`
6. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-api-url.com`
7. Click "Create Static Site"

### Option 5: Cloudflare Pages

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Sign up/login
3. Click "Create a project" → "Connect to Git"
4. Select your repository
5. Configure:
   - Project name: `proteus-frontend`
   - Production branch: `main` (or your main branch)
   - Framework preset: `Vite`
   - Build command: `npm run build`
   - Build output directory: `dist`
6. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-api-url.com`
7. Click "Save and Deploy"

## Important Notes

### Backend API URL

Before deploying, make sure your backend is deployed and accessible. Update the `VITE_API_URL` environment variable with your production backend URL.

**Example:**
- If your backend is on Render: `https://proteus-backend.onrender.com`
- If your backend is on Railway: `https://proteus-backend.railway.app`
- If your backend is on your own server: `https://api.yourdomain.com`

### CORS Configuration

Make sure your backend has CORS configured to allow requests from your frontend domain:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend-domain.vercel.app",  # Add your frontend URL
        "https://your-frontend-domain.netlify.app",  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Testing the Build Locally

Before deploying, test the production build:

```bash
cd client-apps/web-app
npm run build
npm run preview
```

Visit `http://localhost:4173` to test the production build.

## Troubleshooting

### Build Fails

1. Check Node.js version (should be 18+):
   ```bash
   node --version
   ```

2. Clear node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

### API Calls Fail After Deployment

1. Check that `VITE_API_URL` is set correctly in your deployment platform
2. Verify your backend is accessible and CORS is configured
3. Check browser console for errors

### Routes Not Working

If using client-side routing (React Router), you may need to configure redirects:

**For Netlify** - Create `public/_redirects`:
```
/*    /index.html   200
```

**For Vercel** - Create `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

## Quick Deploy Commands

### Vercel (Fastest)
```bash
cd client-apps/web-app
npm i -g vercel
vercel
```

### Netlify
```bash
cd client-apps/web-app
npm i -g netlify-cli
netlify deploy --prod
```

## Need Help?

- Check the build logs in your deployment platform
- Test locally with `npm run build && npm run preview`
- Verify environment variables are set correctly
- Ensure backend is deployed and accessible





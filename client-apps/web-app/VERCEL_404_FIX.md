# Fix 404 on Vercel

If you see **404: NOT_FOUND** after deploying, do these in order.

## 1. Set Root Directory (most common fix)

1. Open [vercel.com](https://vercel.com) → your project.
2. Go to **Settings** → **General**.
3. Find **Root Directory**.
4. Click **Edit**.
5. Type exactly: `client-apps/web-app`  
   (no leading `/`, no trailing `/`, no spaces).
6. Click **Save**.
7. Go to **Deployments** → open the **⋮** menu on the latest deployment → **Redeploy**.

Wait for the new deployment to finish, then open your site URL again.

---

## 2. Check Build & Output

1. **Deployments** → click the latest deployment.
2. Open the **Building** (or **Build Logs**) tab.
3. Confirm:
   - Build runs in `client-apps/web-app` (you should see `npm run build` or Vite).
   - Build **succeeds** (no red errors).
   - **Output Directory** in project Settings → General is `dist` (or leave default if you use our `vercel.json`).

If the build failed or ran in the wrong directory, fix **Root Directory** as in step 1 and redeploy.

---

## 3. Create a New Project (if 404 still happens)

Sometimes starting fresh fixes it:

1. Vercel Dashboard → **Add New** → **Project**.
2. Import the **same** Git repo again.
3. When asked for **Root Directory**, set it to **`client-apps/web-app`** before continuing.
4. Add env vars if needed (e.g. `VITE_API_URL`).
5. Click **Deploy**.
6. Use the new project’s URL (you can delete the old project later).

---

## 4. What we added in the repo

- **404.html** is generated from `index.html` at build time so Vercel can serve the SPA on 404.
- **vercel.json** has `rewrites` so all routes go to `/index.html`.

After any change here, push to Git and let Vercel redeploy, or trigger a **Redeploy** from the dashboard.

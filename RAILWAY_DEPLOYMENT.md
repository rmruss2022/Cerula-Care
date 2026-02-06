# Railway Deployment Guide

This guide will help you deploy the Patient Care Dashboard backend to Railway.

## Step 1: Create Railway Account and Project

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `rmruss2022/Cerula-Care`

## Step 2: Configure the Service

1. Railway will auto-detect it's a Python project
2. Click on the service to configure it
3. Go to **Settings** → **Root Directory**
4. Set Root Directory to: `backend`
5. Go to **Settings** → **Start Command**
6. Set Start Command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

## Step 4: Set Environment Variables

Go to your service **Variables** tab and add:

- `VERCEL_FRONTEND_URL` = `https://frontend-sigma-one-5rg402ltdu.vercel.app` (or your Vercel URL)
- `ALLOWED_ORIGINS` = `http://localhost:3000,http://localhost:5173,https://frontend-sigma-one-5rg402ltdu.vercel.app` (optional, comma-separated)

## Step 5: Seed the Database

After the first deployment:

1. Go to your Railway service
2. Click on the service → **Deployments** tab
3. Click on the latest deployment
4. Click **"View Logs"**
5. Click the **"Shell"** button (or use Railway CLI)

Run the seed script:
```bash
cd backend
python seed_data.py
```

Or use Railway CLI:
```bash
railway run python backend/seed_data.py
```

## Step 6: Get Your Backend URL

1. Go to your Railway service
2. Click on the **"Settings"** tab
3. Under **"Networking"**, you'll see your public URL
4. It will look like: `https://your-app-name.up.railway.app`

## Step 7: Update Vercel Frontend

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add/Update: `VITE_API_URL` = `https://your-app-name.up.railway.app`
4. Go to **Deployments** tab
5. Click the three dots on the latest deployment → **Redeploy**

## Step 8: Verify Deployment

1. Visit your Vercel frontend URL
2. Open browser console (F12) to check for API errors
3. Test the application:
   - View patients list
   - Click on a patient
   - Try creating a new patient
   - Assign care team members
   - View health screening charts

## Troubleshooting

### Database Connection Issues
- Make sure PostgreSQL is added as a service
- Check that `DATABASE_URL` is set automatically
- Verify the database is running

### CORS Errors
- Make sure `VERCEL_FRONTEND_URL` is set correctly
- Check that your Vercel URL is in the `ALLOWED_ORIGINS` or `VERCEL_FRONTEND_URL`

### Port Issues
- Railway automatically sets `$PORT` - make sure your start command uses it
- The Procfile should use `--port $PORT`

### Build Failures
- Check that `requirements.txt` is in the `backend` directory
- Verify all dependencies are listed
- Check Railway build logs for specific errors

## Railway CLI (Optional)

You can also use Railway CLI for easier management:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy
railway up

# View logs
railway logs

# Run commands
railway run python backend/seed_data.py
```

## Environment Variables Summary

**Backend (Railway):**
- `DATABASE_URL` - Auto-set by Railway PostgreSQL
- `VERCEL_FRONTEND_URL` - Your Vercel frontend URL
- `ALLOWED_ORIGINS` - Optional, comma-separated list of allowed origins
- `PORT` - Auto-set by Railway

**Frontend (Vercel):**
- `VITE_API_URL` - Your Railway backend URL

# Deployment Guide

This guide explains how to deploy the Patient Care Dashboard application.

## Architecture

The application consists of two parts:
- **Frontend**: React/TypeScript application (deploy to Vercel)
- **Backend**: FastAPI Python application (deploy to Railway, Render, or Fly.io)

## Frontend Deployment (Vercel)

### Option 1: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Follow the prompts to link your project

5. Set environment variable:
   - Go to your Vercel project settings
   - Add environment variable: `VITE_API_URL` = `https://your-backend-url.com`

### Option 2: Deploy via GitHub Integration

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "New Project"
3. Import your repository: `rmruss2022/Cerula-Care`
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
5. Add environment variable:
   - `VITE_API_URL` = `https://your-backend-url.com`
6. Click "Deploy"

## Backend Deployment

### Option A: Railway (Recommended)

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python
5. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (if needed)
7. Railway will provide a URL like `https://your-app.railway.app`
8. Update your frontend's `VITE_API_URL` to this URL

### Option B: Render

1. Go to [render.com](https://render.com) and sign in
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `cerula-care-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python seed_data.py`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Render will provide a URL
6. Update your frontend's `VITE_API_URL` to this URL

### Option C: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Navigate to backend: `cd backend`
3. Initialize: `fly launch`
4. Create `fly.toml`:
   ```toml
   app = "cerula-care-backend"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[vm]]
     memory_mb = 256
   ```
5. Deploy: `fly deploy`
6. Update your frontend's `VITE_API_URL` to the Fly.io URL

## Post-Deployment Steps

1. **Update CORS**: Make sure your backend allows requests from your Vercel frontend URL
2. **Seed Database**: Run the seed script on your backend deployment
3. **Environment Variables**: Ensure all environment variables are set correctly

## CORS Configuration

If you deploy the backend separately, update `backend/app/main.py` to include your Vercel frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-vercel-app.vercel.app"  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing

After deployment:
1. Visit your Vercel frontend URL
2. Verify it connects to your backend
3. Test all functionality (view patients, create, edit, assign care team, view screenings)

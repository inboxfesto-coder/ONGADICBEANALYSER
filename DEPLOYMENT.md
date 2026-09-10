# Deployment Guide - ONGADICBEANALYSER on Render.com

## Quick Setup (5 minutes)

### Step 1: Create a Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Create a New Web Service
1. Go to your Render dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **ONGADICBEANALYSER** repository
4. Fill in the details:
   - **Name**: `ongadicbeanalyser`
   - **Environment**: Python
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or Starter for paid)

### Step 3: Set Environment Variables
1. Scroll down to **"Environment"**
2. Add these variables:
   - **KEY**: `PYTHON_VERSION` → **VALUE**: `3.11.7`
   - **KEY**: `SECRET_KEY` → **VALUE**: `your-secure-random-string` (generate a strong key!)

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. Wait 5-10 minutes for deployment to complete
4. Your app will be live at: `https://ongadicbeanalyser.onrender.com`

## Database Setup

Your app uses SQLite which stores data locally. To persist data across deployments:

1. **Keep your database in memory** (current setup - data lost on restart)
2. **OR Connect to a PostgreSQL database** (recommended for production)

### Option A: Use Render PostgreSQL (Recommended)
1. Create a PostgreSQL database on Render
2. Add connection string as environment variable
3. Modify `app.py` to use PostgreSQL instead of SQLite

### Option B: Persist SQLite (Not ideal but works)
- Files on Render's free tier are ephemeral (lost on redeploy)
- Data only persists until app restarts

## Important Notes

⚠️ **Security**:
- Change `SECRET_KEY` in production to a random, strong value
- Never commit sensitive keys to GitHub
- Use Render's environment variables for secrets

⚠️ **Database**:
- SQLite on Render's free tier will lose data on redeployment
- For production, use PostgreSQL

⚠️ **Free Tier Limitations**:
- Apps spin down after 15 minutes of inactivity
- Limited resources
- Not suitable for heavy traffic

## Troubleshooting

**App won't start?**
- Check build logs in Render dashboard
- Verify `Procfile` and `requirements.txt` exist
- Ensure Python version is compatible

**Database errors?**
- SQLite database is created automatically on first run
- Check file permissions

**App is slow?**
- Free tier has limited resources
- Upgrade to Starter plan for better performance

---

**Need help?** Check Render docs: https://render.com/docs

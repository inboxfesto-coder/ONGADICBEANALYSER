# RENDER DEPLOYMENT SETUP GUIDE

## Complete Step-by-Step Deployment

This guide walks you through deploying ONGADICBEANALYSER to Render.com with a custom domain.

---

## PART 1: SETUP RENDER ACCOUNT & POSTGRESQL DATABASE

### 1.1 Create Render Account
1. Go to https://render.com
2. Click **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your repositories
5. Complete your profile setup

### 1.2 Create PostgreSQL Database
1. From Render dashboard, click **"New +"** (top-right)
2. Select **"PostgreSQL"**
3. Fill in the details:
   ```
   Name:             ongadicbeanalyser-db
   Database:         ongadi
   User:             ongadi
   Password:         [Auto-generated, save this]
   Region:           [Choose closest to you - e.g., Ohio, Oregon]
   Plan:             Free
   ```
4. Click **"Create Database"**
5. **Wait 2-3 minutes for setup**
6. Once ready, copy the **External Database URL**
   - It looks like: `postgresql://ongadi:password@dpg-xxxx.render.com:5432/ongadi`
   - **Save this - you'll need it soon**

---

## PART 2: CREATE WEB SERVICE

### 2.1 Create Web Service
1. From dashboard, click **"New +"** → **"Web Service"**
2. In "Connect a repository", find `ONGADICBEANALYSER`
3. Click **"Connect"**

### 2.2 Configure Web Service
1. Fill in the basic settings:
   ```
   Name:             ongadicbeanalyser
   Environment:      Python
   Region:           [Same as database]
   Branch:           main
   Runtime:          Python
   Build Command:    pip install -r requirements.txt
   Start Command:    gunicorn app:app
   Plan:             Free
   ```

2. Scroll down to **"Advanced"** section
3. Toggle **"Auto-Deploy"** to ON (for automatic updates when you push)

### 2.3 Set Environment Variables
1. Look for **"Environment"** section
2. Click **"Add Environment Variable"**
3. Add these variables one by one:

   | Variable | Value | Example |
   |----------|-------|---------|
   | `PYTHON_VERSION` | `3.11.7` | `3.11.7` |
   | `SECRET_KEY` | Random string | `abc123xyz789abc123` |
   | `DATABASE_URL` | PostgreSQL URL | `postgresql://ongadi:pass@dpg-xxxx.render.com:5432/ongadi` |

   **How to generate SECRET_KEY:**
   - Use this command in terminal:
     ```bash
     python3 -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
   - Or use an online generator: https://generate-secret.vercel.app/

### 2.4 Create Web Service
1. Click **"Create Web Service"** at the bottom
2. Render will start building (watch the logs)
3. Wait for "✓ Build successful" message
4. App URL will appear: `https://ongadicbeanalyser.onrender.com`

**⏱️ First deployment takes 5-10 minutes**

---

## PART 3: CONFIGURE CUSTOM DOMAIN (OPTIONAL)

### 3.1 Add Custom Domain
1. Go to your Web Service settings
2. Look for **"Custom Domain"** section
3. Click **"Add Custom Domain"**
4. Enter your domain: `yoursite.com` (or subdomain: `app.yoursite.com`)
5. Click **"Add Domain"**
6. Render will show DNS instructions

### 3.2 Configure DNS
If you have a domain (e.g., from GoDaddy, Namecheap):

1. Go to your domain provider's DNS settings
2. Add a **CNAME record**:
   ```
   Type:    CNAME
   Name:    ongadicbeanalyser (or your subdomain)
   Value:   [What Render shows - usually ongadicbeanalyser.onrender.com]
   TTL:     3600
   ```
3. Save DNS settings
4. Wait 5-30 minutes for DNS to propagate
5. Test: Visit your custom domain in browser

---

## PART 4: VERIFY DEPLOYMENT

### 4.1 Check App Status
1. Go to your Web Service dashboard
2. Look for green **"Live"** status
3. Click the URL or visit: `https://ongadicbeanalyser.onrender.com`

### 4.2 Login to Application
1. Default credentials:
   ```
   Username: admin
   Password: admin123
   ```
2. You should see the dashboard with learners and scores

### 4.3 Check Database Connection
1. In Render dashboard, go to PostgreSQL database
2. Check **"Connections"** tab
3. Should see an active connection from your web service

---

## PART 5: POST-DEPLOYMENT TASKS

### 5.1 Change Default Credentials ⚠️
**IMPORTANT: Do this immediately!**

1. Login to your app with `admin / admin123`
2. Navigate to database or admin panel
3. Change the admin password

### 5.2 Enable Database Backups
1. Go to PostgreSQL database settings
2. Enable **"Automated Backups"**
3. Set backup frequency (daily recommended)

### 5.3 Monitor Application
1. Check **"Logs"** regularly for errors
2. Set up alerts if available
3. Monitor database usage

---

## TROUBLESHOOTING

### App Shows "Service Unavailable"
**Solution:**
- Check build logs for errors
- Verify all environment variables are set
- Restart the service (click "Restart" in dashboard)

### Database Connection Failed
**Solution:**
- Verify `DATABASE_URL` in environment variables
- Check if PostgreSQL is running
- Ensure database URL format is correct

### Logs Show "ModuleNotFoundError"
**Solution:**
- Check `requirements.txt` has all dependencies
- Ensure correct spelling and versions
- Push changes and redeploy

### App Spins Down After Inactivity
**This is normal on free tier** - app sleeps after 15 mins with no traffic
- First request after sleep takes 30 seconds
- Upgrade to Starter plan for continuous running

### Changes Not Showing After Push
**Solution:**
- Ensure "Auto-Deploy" is enabled
- Check if build succeeded in logs
- Manually restart if needed

---

## ENVIRONMENT VARIABLES REFERENCE

```bash
# Application Security
SECRET_KEY=your-random-secure-string

# Database Connection (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Python Version
PYTHON_VERSION=3.11.7

# Flask Settings (Optional)
FLASK_ENV=production
```

---

## USEFUL RENDER.COM LINKS

- **Dashboard**: https://dashboard.render.com
- **Web Services**: https://dashboard.render.com/web
- **Databases**: https://dashboard.render.com/databases
- **Logs**: Click your service → "Logs" tab
- **Environment**: Click your service → "Environment" tab

---

## FREQUENTLY ASKED QUESTIONS

### Q: How do I update my code after deployment?
**A:** Just push to GitHub. With auto-deploy enabled, Render automatically redeploys.

### Q: Can I use SQLite instead of PostgreSQL?
**A:** No - SQLite data on Render's free tier is temporary. Use PostgreSQL.

### Q: How much does this cost?
**A:** Free tier available with limitations:
- Free PostgreSQL: 256 MB storage, auto-pauses
- Free Web Service: Auto-spins down after 15 mins inactivity
- Paid plans available for production use

### Q: How do I backup my data?
**A:** PostgreSQL automated backups handle this. Check database settings.

### Q: Can I use a free domain?
**A:** Yes - use a free subdomain from services like:
- https://www.freenom.com
- https://www.nameboy.com
- Or use Render's auto-generated domain

---

## NEXT STEPS

1. ✅ Create Render account
2. ✅ Setup PostgreSQL database
3. ✅ Create web service
4. ✅ Set environment variables
5. ✅ Deploy and verify
6. ✅ Configure custom domain (optional)
7. ✅ Change default credentials
8. ✅ Enable backups
9. ✅ Monitor logs

---

**Your application will be live at:**
- Default: `https://ongadicbeanalyser.onrender.com`
- Custom: `https://your-domain.com`

Good luck with your deployment! 🚀

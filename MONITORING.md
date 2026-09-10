# 📊 MONITORING & MAINTENANCE GUIDE

Keep your ONGADICBEANALYSER application healthy and performing well on Render.com.

---

## DAILY MONITORING (5 minutes)

### Check Application Status
1. Go to https://dashboard.render.com
2. Click your **"ongadicbeanalyser"** web service
3. Look for green **"Live"** status
4. If red or yellow, check logs

### Quick Health Check
```bash
Visit: https://ongadicbeanalyser.onrender.com/health

Should see:
{
  "status": "ok",
  "app": "ONGADI CBE ANALYSER"
}
```

### Monitor Performance
- **Response Time**: Should be <2 seconds
- **Uptime**: Check green indicator
- **Database Connection**: Should be connected

---

## WEEKLY MONITORING (15 minutes)

### Review Application Logs
1. Render Dashboard → Your Web Service
2. Click **"Logs"** tab
3. Look for red error messages
4. Check for patterns/repeated issues

**Common log patterns:**
```
✓ GOOD: "GET /dashboard HTTP/1.1" 200
✓ GOOD: "POST /scores HTTP/1.1" 201
✗ BAD:  "ERROR: Database connection failed"
✗ BAD:  "ModuleNotFoundError"
```

### Check Database Health
1. Go to PostgreSQL database in dashboard
2. Click **"Info"** tab
3. Check:
   - [ ] Status shows "Available"
   - [ ] Memory usage reasonable (<256 MB)
   - [ ] No connection errors
   - [ ] Backups running

### Test Core Features
```
[ ] Login page loads
[ ] Can login with credentials
[ ] Dashboard displays correctly
[ ] Can add learners
[ ] Can record scores
[ ] CSV import works
[ ] Analysis page loads
[ ] Logout works
```

### Monitor Traffic
1. Dashboard → Web Service → **"Metrics"** tab
2. Watch for:
   - CPU usage (should stay below 80%)
   - Memory usage (should stay below 256MB)
   - Request count
   - Error rate (should be 0-5%)

---

## MONTHLY MAINTENANCE (30 minutes)

### Update Dependencies
If using newer versions of Python/dependencies:

```bash
# Check for updates
pip list --outdated

# Update requirements.txt with new versions
pip install --upgrade Flask psycopg2-binary gunicorn

# Save updates
pip freeze > requirements.txt

# Push to GitHub
git add requirements.txt
git commit -m "Update dependencies"
git push origin main

# Render auto-redeploys!
```

### Database Maintenance
1. Go to PostgreSQL database
2. Check **"Backups"** tab:
   - [ ] Automated backups enabled
   - [ ] Latest backup is recent (< 24 hours)
   - [ ] Backup size is reasonable
3. Optional: Download a backup
   ```
   Database Dashboard → Backups → Download
   ```

### Review Security
- [ ] Admin password is secure
- [ ] No sensitive data in logs
- [ ] HTTPS working (🔒 in address bar)
- [ ] Database credentials not exposed
- [ ] Git repo doesn't contain secrets

### Clean Up Old Data
If performance degrades:
```sql
-- Backup first!
-- Then remove old records:
DELETE FROM scores WHERE year < 2024;
DELETE FROM learners WHERE id NOT IN (SELECT DISTINCT learner_id FROM scores);
```

### Performance Optimization
If app is slow:

1. **Clear database:**
   ```sql
   VACUUM; -- Optimize database
   ANALYZE; -- Update statistics
   ```

2. **Restart web service:**
   - Dashboard → Web Service
   - Click **"Restart"**

3. **Check for memory leaks:**
   - Review logs for growing memory
   - Restart if needed

---

## QUARTERLY REVIEW (1 hour)

### Full System Audit
- [ ] All features working
- [ ] No recurring errors
- [ ] Database size reasonable
- [ ] Backups being created
- [ ] HTTPS certificate valid
- [ ] Domain pointing correctly (if custom)
- [ ] Team members can access

### Usage Analytics
1. Check logs for:
   - Most used features
   - Busiest times
   - Error patterns
   - Performance bottlenecks

2. Plan improvements based on:
   - User feedback
   - Usage patterns
   - Performance metrics

### Backup Verification
```bash
1. Download a backup
2. Restore to local testing database
3. Verify data integrity
4. Check all features still work
```

---

## TROUBLESHOOTING GUIDE

### App is Slow
**Symptoms:** Takes >5 seconds to load

**Solution:**
```
1. Check CPU/Memory in Metrics
2. If high (>80%): Restart web service
3. If still slow: Upgrade to Starter plan
4. Check database queries (add indexes if needed)
```

### Database Connection Errors
**Symptoms:** "Connection refused", "Database error"

**Solution:**
```
1. Verify DATABASE_URL environment variable
2. Check PostgreSQL status (should be "Available")
3. Verify network connection allows access
4. Check username/password correct
5. Wait 2-3 minutes if just restarted
```

### High Error Rate
**Symptoms:** Logs show many red errors

**Solution:**
```
1. Check error type in logs
2. If "Module not found": Missing dependency
3. If "Connection failed": Database issue
4. If "Syntax error": Code issue
5. Fix code and push to GitHub
6. Render auto-redeploys
```

### Out of Memory
**Symptoms:** App crashes, metrics show 99% memory

**Solution:**
```
1. Restart web service
2. Check for memory leaks in code
3. Upgrade to Starter plan
4. Clear old data from database
5. Profile application for leaks
```

### SSL Certificate Issues
**Symptoms:** "Connection not secure", warning in browser

**Solution:**
```
1. Wait 5-10 minutes (certificate generating)
2. Clear browser cache
3. Try different browser
4. Check Render dashboard for status
5. If persistent: Contact Render support
```

---

## PERFORMANCE OPTIMIZATION

### Optimize Database Queries
```sql
-- Add indexes for common queries
CREATE INDEX idx_school ON learners(school);
CREATE INDEX idx_learner_id ON scores(learner_id);
CREATE INDEX idx_subject ON scores(subject);

-- These speed up searches significantly
```

### Cache Configuration (Optional)
```python
# In app.py, add caching for better performance
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/dashboard')
@cache.cached(timeout=300)  # Cache for 5 minutes
def dashboard():
    ...
```

### Database Connection Pooling
Already optimized in `app.py` with connection handling.

---

## BACKUP & RECOVERY

### Automated Backups
Render PostgreSQL provides:
- Daily automatic backups
- 7-day retention
- One-click restore

### Manual Backup
1. Dashboard → PostgreSQL database
2. Click **"Backups"**
3. Click **"Backup Now"**
4. Wait for completion
5. Download if needed

### Restore from Backup
1. Go to PostgreSQL database
2. Click **"Backups"** tab
3. Find backup to restore
4. Click **"Restore"**
5. Confirm (data will be overwritten)
6. Wait for restore to complete

---

## MONITORING CHECKLIST

### Daily (5 min)
- [ ] App status is "Live" (green)
- [ ] Can access homepage
- [ ] Login works

### Weekly (15 min)
- [ ] Review logs for errors
- [ ] Test core features
- [ ] Check metrics (CPU/Memory)
- [ ] Database connected
- [ ] Backups created

### Monthly (30 min)
- [ ] Update dependencies if available
- [ ] Review security
- [ ] Database optimization
- [ ] Clean old data

### Quarterly (1 hour)
- [ ] Full system audit
- [ ] Usage analytics review
- [ ] Backup verification
- [ ] Performance tuning

---

## ALERTING SETUP (Optional)

### Email Notifications
Render provides built-in alerts:
1. Dashboard → Web Service
2. Look for **"Notifications"** section
3. Configure alerts for:
   - Service down
   - High CPU usage
   - High memory usage
   - Deploy failures

### Uptime Monitoring
Free services to monitor your app:
- **UptimeRobot**: https://uptimerobot.com
  - Free 5-min checks
  - Email notifications
  - Public status page

- **Ping Bot**: https://pingbot.io
  - Simple uptime checking

Setup:
```
1. Go to UptimeRobot
2. Add monitor
3. URL: https://ongadicbeanalyser.onrender.com/health
4. Check interval: 5 minutes
5. Enable email alerts
```

---

## DOCUMENTATION

### Keep Updated
- [ ] README.md reflects current state
- [ ] Document any customizations
- [ ] Keep credentials secure (use env vars)
- [ ] Record any special configurations

### Team Communication
If multiple users:
- Share access link
- Document username/password changes
- Coordinate updates
- Communicate maintenance windows

---

## CAPACITY PLANNING

### Current Free Tier Limits
```
Web Service:
- 1 CPU core
- 512 MB RAM
- Auto-spins down after 15 min inactivity
- First request takes 30 seconds

PostgreSQL:
- 256 MB storage
- 20 connections max
- Shared backups
```

### When to Upgrade
Consider Starter plan if:
- App needs consistent response time
- High traffic expected
- Database exceeds 256 MB
- 50+ concurrent users
- Production/mission-critical

---

## COMMON ISSUES & SOLUTIONS

| Issue | Cause | Solution |
|-------|-------|----------|
| App slow on first request | Free tier auto-spin-down | Normal; upgrade plan if needed |
| 502 Bad Gateway | Web service crashed | Check logs; restart service |
| Database full | Too much data | Delete old records |
| High memory usage | Memory leak | Restart service |
| Connection timeout | Network issue | Check database; wait 1-2 min |
| SSL warning | Certificate issue | Wait 10 min; refresh browser |
| Login fails | Database issue | Check DB connection |
| CSV import fails | File format issue | Check CSV format (headers required) |

---

## DISASTER RECOVERY

### If Everything Goes Down

1. **Check status:**
   ```
   Go to Render dashboard
   Look at service status
   Check logs for error messages
   ```

2. **Restart service:**
   ```
   Dashboard → Web Service → Restart
   Wait 2 minutes
   Check status
   ```

3. **If database issue:**
   ```
   Go to PostgreSQL database
   Check status
   If available: Restart didn't help
   Restore from backup (if needed)
   ```

4. **Still broken:**
   ```
   Contact Render support
   Provide error logs
   Describe what happened
   Wait for response (1-24 hours)
   ```

---

## OPTIMIZATION TIPS

### For Better Performance
1. Add database indexes (see above)
2. Implement caching
3. Optimize images/files
4. Minimize database queries
5. Use CDN for static files

### For Better Security
1. Use strong passwords
2. Enable 2FA on Render account
3. Rotate secrets periodically
4. Don't commit sensitive data
5. Use environment variables

### For Better Reliability
1. Enable automated backups
2. Test backups monthly
3. Monitor uptime
4. Keep dependencies updated
5. Document configurations

---

## USEFUL COMMANDS

### Check app health from terminal
```bash
curl https://ongadicbeanalyser.onrender.com/health

# Should return:
# {"status": "ok", "app": "ONGADI CBE ANALYSER"}
```

### Generate strong SECRET_KEY
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Test database connection
```bash
psql postgresql://ongadi:PASSWORD@host:5432/ongadi
# Should connect without errors
```

---

## SUPPORT RESOURCES

| Resource | Link |
|----------|------|
| Render Docs | https://render.com/docs |
| Render Status | https://status.render.com |
| Render Support | https://render.com/contact |
| Flask Docs | https://flask.palletsprojects.com |
| PostgreSQL Docs | https://www.postgresql.org/docs |
| Gunicorn Docs | https://gunicorn.org |

---

## MONITORING SCHEDULE TEMPLATE

```
DAILY:
[ ] Check app status - _______ (time)
[ ] Test login - _______ (time)

WEEKLY:
[ ] Review logs - _______ (day/time)
[ ] Test features - _______ (day/time)
[ ] Check metrics - _______ (day/time)

MONTHLY:
[ ] Update dependencies - _______ (date)
[ ] Database maintenance - _______ (date)
[ ] Security review - _______ (date)
[ ] Clean old data - _______ (date)

QUARTERLY:
[ ] Full audit - _______ (quarter/date)
[ ] Backup verification - _______ (quarter/date)
[ ] Performance review - _______ (quarter/date)
```

---

## NOTES

```
Last Checked: _________________
Issues Found: _________________
Actions Taken: _________________
Next Review: _________________
```

---

**Your app is now fully monitored and maintained!** 📊

Keep checking regularly to ensure optimal performance. 🚀

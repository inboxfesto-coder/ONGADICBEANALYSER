# CUSTOM DOMAIN SETUP GUIDE

Complete guide to configure a custom domain for your ONGADICBEANALYSER application on Render.com.

---

## Option 1: FREE DOMAIN SETUP

### Using Freenom (Free .tk, .ml, .ga, .cf domains)

#### Step 1: Register Free Domain
1. Go to https://www.freenom.com
2. Click **"Find your new domain"**
3. Search for: `ongadicbeanalyser.tk` (or similar)
4. Click **"Get it now"**
5. Add to cart and checkout
6. Create account and verify email
7. Confirm order (12-month free)

#### Step 2: Set DNS Records on Freenom
1. Login to Freenom
2. Go to **"Services"** → **"My Domains"**
3. Click **"Manage Domain"** for your domain
4. Click **"Management Tools"** → **"Nameservers"**
5. Select **"Use custom nameservers"**
6. Add Render's nameservers (or use CNAME below)

---

## Option 2: CUSTOM DOMAIN (Paid - Recommended)

### Popular Domain Registrars
- GoDaddy: https://godaddy.com
- Namecheap: https://namecheap.com
- Google Domains: https://domains.google.com
- Bluehost: https://bluehost.com

#### Step 1: Register Domain
1. Choose a registrar above
2. Search for your domain: `ongadi-cbe.com` or similar
3. Purchase annual subscription
4. Note your domain name

---

## CONNECT DOMAIN TO RENDER

### Step 1: Add Domain to Render Web Service
1. Go to Render dashboard
2. Click your **"ongadicbeanalyser"** web service
3. Scroll to **"Custom Domain"** section
4. Click **"Add Custom Domain"**
5. Enter your domain: `ongadi-cbe.com` or `app.ongadi-cbe.com`
6. Click **"Add Domain"**
7. Render shows DNS setup instructions

### Step 2: Configure DNS Records

#### Option A: CNAME Record (Easiest)
If your domain registrar allows CNAME at root:

1. Go to your domain registrar's DNS settings
2. Create a **CNAME** record:
   ```
   Type:        CNAME
   Name/Host:   @ (or leave blank for root domain)
   Value:       ongadicbeanalyser.onrender.com
   TTL:         3600 (or auto)
   ```
3. Save and wait 5-30 minutes

#### Option B: Nameserver Records (More Control)
If CNAME doesn't work:

1. Go to your domain registrar's DNS settings
2. Find "Nameservers" section
3. Replace existing nameservers with Render's nameservers
4. Render provides these in setup instructions
5. Wait 24-48 hours for propagation

#### Option C: A Record (IP Address)
For registrars requiring A records:

1. Get Render's IP address (shown in domain setup)
2. Create A record:
   ```
   Type:        A
   Name/Host:   @ (or subdomain)
   Value:       [Render's IP address]
   TTL:         3600
   ```
3. Save and wait 5-30 minutes

### Step 3: Verify Domain Setup
1. Wait 5-30 minutes for DNS propagation
2. Go to Render dashboard
3. Check domain status (should show "Active")
4. Visit your domain in browser
5. Should see your ONGADICBEANALYSER app

---

## DOMAIN SETUP FOR SPECIFIC REGISTRARS

### GoDaddy
1. Login to GoDaddy account
2. Click **"Manage All"** → Find your domain
3. Click the domain name
4. Click **"DNS"** tab
5. Under "Records", add:
   ```
   Type:        CNAME
   Name:        ongadi (if subdomain: app.ongadi-cbe.com, use "app")
   Value:       ongadicbeanalyser.onrender.com
   TTL:         3600
   ```
6. Save changes
7. Done! (Usually takes 5-30 minutes)

### Namecheap
1. Login to Namecheap
2. Click **"Domain List"**
3. Click **"Manage"** next to your domain
4. Click **"Advanced DNS"** tab
5. Add new record:
   ```
   Type:        CNAME Record
   Host:        ongadi (or subdomain)
   Value:       ongadicbeanalyser.onrender.com
   TTL:         3600
   ```
6. Save changes
7. Done!

### Google Domains
1. Go to https://domains.google.com
2. Click your domain
3. Click **"DNS"** in left menu
4. Scroll to **"Custom records"**
5. Add new record:
   ```
   Type:        CNAME
   Data:        ongadicbeanalyser.onrender.com
   ```
6. Save changes
7. Done!

### Bluehost
1. Login to Bluehost
2. Click **"Domains"**
3. Click your domain
4. Click **"DNS"** tab
5. Add CNAME record as above
6. Save changes

---

## TESTING YOUR DOMAIN

### Check DNS Propagation
1. Use online tool: https://dnschecker.org
2. Enter your domain
3. Check if CNAME points to Render
4. Should show: `ongadicbeanalyser.onrender.com`

### Test HTTPS Certificate
1. Visit your domain (e.g., https://ongadi-cbe.com)
2. Check browser address bar for lock icon 🔒
3. HTTPS should be automatic

### Common Issues

**Domain shows old website:**
- DNS not propagated yet
- Wait 24-48 hours and try again
- Clear browser cache

**SSL Certificate Error:**
- Wait 5-10 minutes for certificate generation
- Refresh page
- Check Render dashboard for status

**"Can't connect to server":**
- Verify CNAME record in DNS
- Use https://dnschecker.org to verify
- Check Render web service is running

---

## REDIRECT HTTP to HTTPS

Render automatically redirects, but ensure in your app's settings:

In Render dashboard:
1. Go to Web Service
2. Look for **"HTTPS"** section
3. Ensure **"Redirect HTTP to HTTPS"** is enabled

---

## EMAIL FORWARDING (Optional)

If you want email from your domain:

### Using Namecheap Email Forwarding (Free)
1. Go to Namecheap domain settings
2. Find **"Email Forwarding"**
3. Add forwarding rule:
   ```
   From:  info@ongadi-cbe.com
   To:    your-real-email@gmail.com
   ```
4. Save
5. Test by sending email to info@ongadi-cbe.com

---

## RENEW DOMAIN

### Before Expiration
1. Login to registrar
2. Find domain renewal option
3. Renew for 1-3 years
4. Pay renewal fee
5. Continue using normally

**Tip:** Set auto-renewal if available to avoid expiration

---

## TROUBLESHOOTING CUSTOM DOMAIN

| Problem | Solution |
|---------|----------|
| Domain not working | Wait 24-48 hours for DNS propagation |
| Shows old content | Clear browser cache (Ctrl+Shift+Del) |
| SSL error | Wait 5-10 min for certificate, refresh page |
| CNAME not recognized | Verify correct spelling in DNS records |
| Domain provider error | Contact their support, verify credentials |
| Still showing Render domain | Check Render dashboard shows custom domain as "Active" |

---

## COMPARISON: FREE vs PAID DOMAINS

| Feature | Free (.tk/.ml) | Paid (.com/.net) |
|---------|---|---|
| Cost/Year | $0 | $10-15 |
| Reliability | Lower | Higher |
| Trust | Lower | Higher |
| Renewal | Yearly manual | Auto or manual |
| Professional | No | Yes |
| Email | Limited | Usually included |

**Recommendation:** Use paid domain for production/professional use

---

## USEFUL LINKS

- **Render Domain Setup**: https://render.com/docs/custom-domains
- **DNS Checker**: https://dnschecker.org
- **CNAME Lookup**: https://mxtoolbox.com/cname.aspx
- **HTTP Headers Check**: https://httpheader.toolforge.org/

---

## DOMAIN SETUP CHECKLIST

- [ ] Register domain (free or paid)
- [ ] Add domain to Render web service
- [ ] Configure DNS records (CNAME/A record)
- [ ] Wait for DNS propagation (5 min - 48 hours)
- [ ] Test domain in browser (https://your-domain.com)
- [ ] Verify HTTPS certificate (🔒 in address bar)
- [ ] Check DNS using dnschecker.org
- [ ] Test application functionality
- [ ] Set auto-renewal on registrar
- [ ] Update any documentation with new domain

---

**Your custom domain is now live!** 🎉

Visit: `https://your-domain.com`

For issues, check:
1. Render dashboard - domain status
2. DNS records - CNAME/A record
3. DNS propagation - use dnschecker.org
4. Browser cache - clear and refresh

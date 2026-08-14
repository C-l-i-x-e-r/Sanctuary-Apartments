# 🚀 DEPLOYMENT - Get Your Public Link (5 Minutes)

## ⚡ FASTEST METHOD: Railway.app (Recommended)

### Step 1: Go to Railway
Visit: https://railway.app

### Step 2: Create New Project
- Click "**Create New Project**"
- Select "**Deploy from GitHub**" OR "**Empty Project**"

### Step 3A: If Using GitHub (Recommended)
1. Create new GitHub repo (https://github.com/new)
2. Upload these files:
   - `sanctuary_app.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.env`
   - `/templates/` folder
   - `/static/` folder

3. In Railway: Connect to your GitHub repo

### Step 3B: If Using Direct Upload
1. In Railway: Click "Empty Project"
2. Upload all files above in the file manager

### Step 4: Deploy
1. Railway detects `Procfile` automatically
2. Click "Deploy"
3. Wait 2-3 minutes
4. Your public URL appears (example: `sanctuary-apts.up.railway.app`)

### Step 5: Access Your App
Your **public link**: `https://[your-project-name].up.railway.app`

Login with:
- **Username**: `admin`
- **Password**: `gordonramsey`

---

## Alternative: Render.com

### Step 1: Visit https://render.com
- Sign up free

### Step 2: Create Web Service
- Click "**New +"** → "**Web Service**"
- Select "**Public Git Repository**"
- Paste: `https://github.com/YOUR-USERNAME/REPO-NAME`

### Step 3: Configure
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python sanctuary_app.py`

### Step 4: Deploy & Get URL
Render automatically assigns you a public URL

---

## Alternative: Replit

### Step 1: Visit https://replit.com
- Sign up free

### Step 2: Create New Repl
- Click "**Create Repl**"
- Select "**Python**" as language

### Step 3: Upload Files
- Upload all files from your project

### Step 4: Run
- Click the "**Run**" button
- Replit automatically creates a public URL

---

## ✅ Final Result

After deployment, you'll have:
- **Public URL**: Works on any device/browser
- **32 Apartment Units**: Fully functional listing
- **Admin Account**: admin/gordonramsey
- **User Registration**: Anyone can create accounts
- **Secure**: HTTPS with security headers

---

## 🔑 Admin Credentials
- **Username**: `admin`
- **Password**: `gordonramsey`

**IMPORTANT**: Change this password after first login!

---

## 📱 Testing URLs
Once deployed, try:
- **Login**: `https://[your-url]/login`
- **Register**: `https://[your-url]/register`
- **Dashboard**: `https://[your-url]/dashboard`
- **Admin Panel**: `https://[your-url]/admin`
- **Unit Details**: `https://[your-url]/unit/1`

---

## ⚠️ Configuration in Deployed Environment

Make sure `.env` file has:
```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=generate-random-key-here
DATABASE_URI=sqlite:///sanctuary.db
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
RATELIMIT_ENABLED=True
```

Railway/Render automatically sets `PORT` environment variable - no configuration needed!

---

## 🆘 Need Help?

If deployment fails:
1. Check all required files exist (sanctuary_app.py, requirements.txt, Procfile)
2. Verify requirements.txt has all dependencies
3. Check logs in your deployment platform
4. Make sure PORT is read from environment (already configured ✓)

**Your app is production-ready!** 🎉

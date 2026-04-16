# Railway Deployment Guide

## ✅ Super Simple Setup (5 minutes)

### Step 1: Go to Railway
1. Open: https://railway.app
2. Click **"Start Project"**
3. Select **"Deploy from GitHub repo"**

### Step 2: Connect GitHub & Select Repo
1. Click **"GitHub"** to authorize
2. Select your repository: **`nepse-portfolio-app`**
3. Railway will auto-detect the structure

### Step 3: Railway Auto-Setup
Railway will automatically:
- ✅ Detect Python backend (FastAPI)
- ✅ Detect React frontend
- ✅ Create services for both
- ✅ Deploy both services

### Step 4: Add Environment Variables

Once deployed, go to **Backend service** settings:

1. Click on **Backend service** in your Railway project
2. Go to **"Variables"** tab
3. Add these variables:

```
TELEGRAM_BOT_TOKEN=8519550594:AAGWOElqwgIWGPdX4w8AFaMKV8w54J_DGGs
TELEGRAM_CHAT_ID=7540683688
NEPSE_API_BASE=https://www.nepseapi.surajrimal.dev
ENVIRONMENT=production
```

4. Click **"Deploy"** to restart with new variables

### Step 5: Get Your URLs

After deployment completes, you'll see:
- **Backend URL**: `https://your-app-backend.railway.app`
- **Frontend URL**: `https://your-app-frontend.railway.app`

### Step 6: Update Frontend to Use Backend URL

1. In Railway, go to **Frontend service**
2. Go to **"Variables"** tab
3. Add:
```
VITE_API_URL=https://your-app-backend.railway.app
```
(Replace with actual backend URL from step 5)

4. Click **"Deploy"** to restart

---

## 🌐 Connect Custom Domain (meroshare.live)

### For Frontend:
1. Railway Dashboard → Frontend service
2. **"Settings"** → **"Custom Domain"**
3. Enter: `meroshare.live`
4. Railway shows you a CNAME record
5. Go to Hostinger:
   - Domain → **DNS Zone**
   - Add CNAME as shown by Railway
6. Wait 24-48 hours for DNS propagation

### For Backend (Optional):
1. Create subdomain: `api.meroshare.live`
2. Same steps as frontend
3. CNAME points to backend URL

---

## ✅ Verification

Once DNS propagates:
- ✅ Visit: **meroshare.live** → Should see your app
- ✅ Backend at: **api.meroshare.live/api/v1/stocks/list**
- ✅ Portfolio management working
- ✅ Telegram alerts sending

---

## 💰 Cost

- **Free tier**: $5/month credits
- **Your app usage**: ~$1-2/month
- **Result**: Completely free! ✅

---

## 🔄 Auto-Deploy

Every time you push to GitHub:
```bash
git commit -am "your message"
git push origin main
```

Railway automatically redeploys! 🎯

---

## 📋 Troubleshooting

**App not starting?**
- Check Railway **"Logs"** tab for errors

**Environment variables not working?**
- Make sure to **"Deploy"** after adding variables
- Check backend is restarted

**Domain not resolving?**
- Wait 24-48 hours for DNS
- Check CNAME record is correct in Hostinger

**Frontend can't reach backend?**
- Make sure `VITE_API_URL` is set correctly
- Check frontend is restarted after variable change

---

## 🚀 Quick Start

1. https://railway.app
2. Sign in with GitHub
3. Select your repo
4. Wait for auto-deployment
5. Add environment variables
6. Update frontend API URL
7. Connect custom domain
8. Done! ✅

**Total time: ~15 minutes**

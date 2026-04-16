# ⚡ Quick Azure Setup (5 Minutes)

## Option A: Automatic Setup (Recommended) ✅

### Step 1: Open Terminal and Login
```powershell
az login
```
This opens your browser to login with your university account.

### Step 2: Run Setup Script
```powershell
cd "d:\NEPSE Project"
./azure-setup.ps1
```

This will automatically create:
- ✅ Resource Group (nepse-rg)
- ✅ App Service Plan (nepse-plan)  
- ✅ Backend App Service (nepse-backend-api)
- ✅ Frontend Static Web App (nepse-frontend)

**Duration: 3-5 minutes**

---

## Option B: Manual Setup (Azure Portal)

### Step 1: Create Resource Group
1. Go to https://portal.azure.com
2. Search for **"Resource groups"**
3. Click **"Create"**
4. **Subscription**: Your student subscription
5. **Resource group name**: `nepse-rg`
6. **Region**: East US
7. Click **"Review + Create"** → **"Create"**

### Step 2: Create App Service Plan
1. Search for **"App Service plans"**
2. Click **"Create"**
3. **Resource group**: nepse-rg
4. **Name**: nepse-plan
5. **Operating System**: Linux
6. **Region**: East US
7. **SKU and size**: Free (F1)
8. Click **"Review + Create"** → **"Create"**

### Step 3: Create Backend App Service
1. Search for **"App Services"**
2. Click **"Create"**
3. **Resource group**: nepse-rg
4. **Name**: nepse-backend-api
5. **Publish**: Code
6. **Runtime stack**: Python 3.11
7. **Operating System**: Linux
8. **App Service plan**: nepse-plan
9. Click **"Review + Create"** → **"Create"**

### Step 4: Configure Backend Environment Variables
1. Go to the created App Service
2. **Settings** → **Configuration**
3. Click **"New application setting"**
4. Add these settings:
   ```
   TELEGRAM_BOT_TOKEN = 8519550594:AAGWOElqwgIWGPdX4w8AFaMKV8w54J_DGGs
   TELEGRAM_CHAT_ID = 7540683688
   NEPSE_API_BASE = https://www.nepseapi.surajrimal.dev
   ENVIRONMENT = production
   ```
5. Click **"Save"**

### Step 5: Create Static Web App (Frontend)
1. Search for **"Static Web Apps"**
2. Click **"Create"**
3. **Resource group**: nepse-rg
4. **Name**: nepse-frontend
5. **Hosting plan**: Free
6. **Region**: East US
7. **Source**: GitHub (you'll authorize GitHub)
8. **Organization**: ashiishmahato
9. **Repository**: nepse-portfolio-app
10. **Branch**: main
11. **Build presets**: React
12. **App location**: /frontend
13. **Output location**: dist
14. Click **"Review + Create"** → **"Create"**

### Step 6: Get Deployment Credentials
1. Go to **nepse-backend-api** App Service
2. **Deployment** → **Deployment center**
3. **GitHub Actions** tab
4. Click **"Disconnect"** then **"Connect"** to set up CI/CD
5. Azure will create GitHub secrets automatically

Or manually:
1. **nepse-backend-api** → Overview
2. Click **"Download publish profile"**
3. Go to GitHub: Settings → Secrets → New secret
4. Name: `AZURE_APPSERVICE_PUBLISH_PROFILE`
5. Paste the XML content

---

## ✅ Verification

### Frontend is Ready When:
- You see: nepse-frontend.azurestaticapps.net
- GitHub Actions shows ✅ completed deployment

### Backend is Ready When:
- You see: nepse-backend-api.azurewebsites.net
- Can access: https://nepse-backend-api.azurewebsites.net/api/v1/stocks/list

---

## 🌐 Connect Custom Domain (meroshare.live)

### For Frontend (Static Web App)
1. **nepse-frontend** → **Settings** → **Custom domains**
2. Click **"Add"**
3. Enter: `meroshare.live`
4. Azure shows CNAME record
5. Go to Hostinger:
   - Domain → DNS Zone
   - Add CNAME as shown
6. Wait 24-48 hours for DNS propagation

### For Backend (Optional)
1. Create subdomain: `api.meroshare.live`
2. **nepse-backend-api** → **Settings** → **Custom domains**
3. Add CNAME in Hostinger DNS

---

## 📱 GitHub Secrets Setup

After Azure creates resources, add these GitHub secrets:
https://github.com/ashiishmahato/nepse-portfolio-app/settings/secrets/actions

```
AZURE_APPSERVICE_NAME = nepse-backend-api
AZURE_APPSERVICE_PUBLISH_PROFILE = (paste XML from download)
AZURE_STATIC_WEB_APPS_API_TOKEN = (get from Static Web App deployment settings)
```

---

## 🧪 Test Deployment

Push a change to trigger deployment:
```bash
cd "d:\NEPSE Project"
git commit --allow-empty -m "Trigger deployment"
git push origin main
```

Monitor in GitHub → **Actions** tab

---

## 💬 Support

**Issues?**
- Backend not starting: Check **Log stream** in App Service
- Frontend not building: Check GitHub Actions build logs
- Domain not working: Run `nslookup meroshare.live`

---

**Total time: 10-15 minutes** ⏱️
**Total cost: $0** 💰

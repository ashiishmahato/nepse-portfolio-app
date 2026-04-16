# Azure Deployment Guide for NEPSE Portfolio App

## Prerequisites
- Azure Student Account (with $100 credits or $75 depending on region)
- GitHub account with repository pushed ✅
- Your domain: meroshare.live

## Step 1: Deploy Frontend to Azure Static Web Apps

### 1.1 Create Static Web App
1. Go to Azure Portal: https://portal.azure.com
2. Search for **"Static Web Apps"**
3. Click **"Create"**
4. Fill in:
   - **Subscription**: Your student subscription
   - **Resource Group**: Create new → `nepse-rg`
   - **Name**: `nepse-frontend`
   - **Plan Type**: Free
   - **Region**: East US (or closest to you)
   - **Deployment details**:
     - Source: GitHub
     - Organization: ashiishmahato
     - Repository: nepse-portfolio-app
     - Branch: main
   - **Build Presets**: React
   - **App location**: `/frontend`
   - **Output location**: `dist`

5. Click **"Review + Create"** → **"Create"**
6. Wait for deployment (2-3 minutes)

### 1.2 Get API Token from Static Web App
1. Once created, go to **Settings** → **Configuration**
2. Copy the **Deployment token**
3. Save it somewhere safe (you'll need it for GitHub)

### 1.3 Add Secret to GitHub
1. Go to GitHub: https://github.com/ashiishmahato/nepse-portfolio-app
2. Settings → Secrets and variables → Actions
3. Click **"New repository secret"**
4. Name: `AZURE_STATIC_WEB_APPS_API_TOKEN`
5. Value: Paste the deployment token from Step 1.2
6. Click **"Add secret"**

---

## Step 2: Deploy Backend to Azure App Service

### 2.1 Create App Service Plan
1. Azure Portal → Search **"App Services"**
2. Click **"Create"**
3. Fill in:
   - **Subscription**: Your student subscription
   - **Resource Group**: `nepse-rg` (same as frontend)
   - **Name**: `nepse-backend-api`
   - **Publish**: Code
   - **Runtime stack**: Python 3.11
   - **Operating System**: Linux
   - **Region**: East US
   - **App Service Plan**:
     - Click **"Create new"** → `nepse-plan`
     - SKU: Free (F1)

4. Click **"Review + Create"** → **"Create"**
5. Wait for deployment

### 2.2 Configure App Service
1. Go to the App Service → **Settings** → **Configuration**
2. Add Application settings:
   - `TELEGRAM_BOT_TOKEN`: Your bot token (8519550594:AAGWOElqwgIWGPdX4w8AFaMKV8w54J_DGGs)
   - `TELEGRAM_CHAT_ID`: Your chat ID (7540683688)
   - `NEPSE_API_BASE`: https://www.nepseapi.surajrimal.dev
   - `ENVIRONMENT`: production
3. Click **"Save"**

### 2.3 Get Publish Profile
1. App Service → **Overview** → **Download publish profile**
2. This is an XML file - keep it safe

### 2.4 Add Secret to GitHub
1. GitHub Settings → Secrets and variables → Actions
2. Click **"New repository secret"**
3. Name: `AZURE_APPSERVICE_PUBLISH_PROFILE`
4. Value: Copy entire content of the XML publish profile file
5. Click **"Add secret"**

### 2.5 Add App Service Name to GitHub Secret
1. GitHub Settings → Secrets and variables → Actions
2. Click **"New repository secret"**
3. Name: `AZURE_APPSERVICE_NAME`
4. Value: `nepse-backend-api` (from Step 2.1)
5. Click **"Add secret"**

---

## Step 3: Connect Custom Domain

### 3.1 For Frontend (Static Web App)
1. Azure Portal → Static Web App → **Settings** → **Custom domains**
2. Click **"Add"** → **"Custom domain"**
3. Enter: `meroshare.live`
4. Azure will show you DNS records to add
5. Go to Hostinger:
   - Domain → DNS Zone
   - Add CNAME record as shown by Azure
6. Click **"Add"** and wait 24-48 hours for propagation

### 3.2 For Backend (App Service) - Optional
1. Create subdomain: `api.meroshare.live`
2. App Service → **Settings** → **Custom domains**
3. Add `api.meroshare.live`
4. Configure in Hostinger DNS similarly

---

## Step 4: Enable HTTPS & Set Managed Certificates

### Frontend
1. Static Web App → **Settings** → **Custom domains**
2. Click your domain → **HTTPS** should be automatic

### Backend
1. App Service → **Settings** → **SSL settings**
2. Select **"App Service managed certificate"**
3. Click **"Add binding"**
4. Select HTTPS binding

---

## Step 5: Test Deployment

### Push code to trigger deployment:
```bash
cd d:\NEPSE Project
git add .
git commit -m "Add Azure deployment workflows"
git push origin main
```

This will trigger:
- ✅ Frontend deployment (GitHub Actions → Static Web Apps)
- ✅ Backend deployment (GitHub Actions → App Service)

### Monitor deployment:
1. GitHub → Actions tab → Watch workflows run
2. Azure Portal → Resource Group → Monitor resources
3. Frontend: nepse-frontend.azurestaticapps.net
4. Backend: nepse-backend-api.azurewebsites.net

---

## Step 6: Update Frontend API URLs

Frontend needs to know backend URL. Update in `frontend/src/services/api.js`:

```javascript
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://nepse-backend-api.azurewebsites.net'
  : 'http://localhost:8000';
```

---

## Environment Variables Reference

### Backend (.env on App Service)
```
TELEGRAM_BOT_TOKEN=8519550594:AAGWOElqwgIWGPdX4w8AFaMKV8w54J_DGGs
TELEGRAM_CHAT_ID=7540683688
NEPSE_API_BASE=https://www.nepseapi.surajrimal.dev
ENVIRONMENT=production
```

### Frontend (.env.local for local testing)
```
VITE_API_URL=https://nepse-backend-api.azurewebsites.net
```

---

## Troubleshooting

**Frontend not updating?**
- Check Static Web App build logs in Azure Portal
- Ensure `frontend/dist` folder is correctly built

**Backend deployment fails?**
- Check App Service logs: Monitoring → Log stream
- Verify Python 3.11 runtime is selected
- Ensure all requirements.txt packages are compatible with Linux

**Domain not working?**
- Wait for DNS propagation (up to 48 hours)
- Clear browser cache
- Test with `nslookup meroshare.live`

---

## Next Steps

1. ✅ Push code to GitHub
2. 🔄 Follow steps above to set up Azure resources
3. 🔄 Add GitHub secrets
4. 🔄 Update frontend API URL
5. ✅ Watch deployments in GitHub Actions
6. 🔄 Test at meroshare.live

**Total setup time: ~30 minutes**
**Monthly cost: $0 (free tier)**

---

## Support Commands

```bash
# Check what's deployed
git log --oneline

# Redeploy latest
git commit --allow-empty -m "Trigger redeployment"
git push origin main

# View workflow status
# GitHub → Actions tab
```

---

**Questions? Let me know!** 🚀

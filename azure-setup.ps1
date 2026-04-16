# NEPSE App - Manual Azure Setup Guide
# Run this after logging in: az login

# Set variables
$resourceGroup = "nepse-rg"
$location = "eastus"
$frontendAppName = "nepse-frontend"
$backendAppName = "nepse-backend-api"
$appServicePlan = "nepse-plan"

Write-Host "🚀 Starting Azure Resource Creation..." -ForegroundColor Green

# 1. Create Resource Group
Write-Host "`n📦 Creating Resource Group: $resourceGroup..." -ForegroundColor Cyan
az group create --name $resourceGroup --location $location

# 2. Create App Service Plan (Free tier)
Write-Host "`n🔧 Creating App Service Plan: $appServicePlan..." -ForegroundColor Cyan
az appservice plan create `
    --name $appServicePlan `
    --resource-group $resourceGroup `
    --is-linux `
    --sku F1

# 3. Create Backend App Service (Python)
Write-Host "`n🐍 Creating Backend App Service: $backendAppName..." -ForegroundColor Cyan
az webapp create `
    --resource-group $resourceGroup `
    --plan $appServicePlan `
    --name $backendAppName `
    --runtime "python|3.11"

# 4. Configure Backend App Service settings
Write-Host "`n⚙️  Configuring Backend Environment Variables..." -ForegroundColor Cyan
az webapp config appsettings set `
    --resource-group $resourceGroup `
    --name $backendAppName `
    --settings `
    TELEGRAM_BOT_TOKEN="8519550594:AAGWOElqwgIWGPdX4w8AFaMKV8w54J_DGGs" `
    TELEGRAM_CHAT_ID="7540683688" `
    NEPSE_API_BASE="https://www.nepseapi.surajrimal.dev" `
    ENVIRONMENT="production" `
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# 5. Create Static Web App (Frontend)
Write-Host "`n⚡ Creating Static Web App: $frontendAppName..." -ForegroundColor Cyan
az staticwebapp create `
    --name $frontendAppName `
    --resource-group $resourceGroup `
    --source "https://github.com/ashiishmahato/nepse-portfolio-app" `
    --location $location `
    --branch "main" `
    --app-location "frontend" `
    --output-location "dist" `
    --login-with-github

Write-Host "`n✅ Azure Resources Created Successfully!" -ForegroundColor Green

# Display resource details
Write-Host "`n📋 Resource Details:" -ForegroundColor Yellow
Write-Host "Resource Group: $resourceGroup"
Write-Host "Backend URL: https://$backendAppName.azurewebsites.net"
Write-Host "Frontend URL: https://$frontendAppName.azurestaticapps.net"

Write-Host "`n📝 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Get Backend Publish Profile:"
Write-Host "   az webapp deployment list-publishing-profiles --resource-group $resourceGroup --name $backendAppName --xml > publish-profile.xml"
Write-Host ""
Write-Host "2. Add GitHub Secrets:"
Write-Host "   - AZURE_APPSERVICE_PUBLISH_PROFILE: (content of publish-profile.xml)"
Write-Host "   - AZURE_APPSERVICE_NAME: $backendAppName"
Write-Host ""
Write-Host "3. Configure Custom Domain (meroshare.live)"
Write-Host ""
Write-Host "✨ Deployment scripts are ready in .github/workflows/"

Read-Host "`nPress Enter to finish"

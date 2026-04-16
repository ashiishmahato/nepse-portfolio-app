# Quick Start Guide

Get Smart NEPSE Investor running in 5 minutes!

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git (optional)

## Step 1: Setup Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

Open in browser: http://localhost:8000/docs (Interactive API docs)

## Step 2: Setup Frontend (2 minutes)

In a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: http://localhost:3000

## Step 3: Initialize Data (1 minute)

Visit this URL in your browser to populate the database:

```
http://localhost:8000/api/v1/stocks/initialize
```

You should see:
```json
{
  "message": "Database initialized successfully",
  "stocks_added": 10,
  "historical_data_days": 200
}
```

## Step 4: Start Using

1. Open http://localhost:3000 in your browser
2. Explore the Dashboard
3. Go to Portfolio page and click "Add Stock"
4. Add a stock, set target profit, and submit
5. Check Alerts page for generated signals

## Step 5: (Optional) Start Background Scheduler

In another terminal:

```bash
cd backend
python scheduler.py
```

This will automatically:
- Update prices every 1 minute
- Calculate analysis every 5 minutes
- Generate alerts every 2 minutes

---

## What Each Page Does

### Dashboard
- Portfolio summary (total invested, current value, profit/loss)
- Active alerts count
- Recent holdings
- Top recommended stocks

### Portfolio
- View all stock holdings
- Add new stocks
- Edit targets and stop loss
- Sell positions

### Stocks
- Browse all available NEPSE stocks
- View current prices
- See technical analysis scores
- Search and filter stocks

### Alerts
- View all active alerts
- Filter by alert type
- Mark alerts as read
- Manually generate alerts

---

## Adding Your First Stock

1. Click "Portfolio" in navigation
2. Click "Add Stock" button
3. Fill in:
   - **Stock Symbol**: NABIL (from dropdown)
   - **Buy Price**: 1400
   - **Quantity**: 10
   - **Target Profit %**: 15
   - **Stop Loss %**: 10 (optional)
4. Click "Add to Portfolio"

Now your position will appear in:
- Portfolio page
- Dashboard summary
- Alerts will be generated automatically

---

## Understanding the UI

### Color Coding
- 🟢 **Green**: Profit, Buy signal, High volume
- 🔴 **Red**: Loss, Sell signal, Stop loss
- 🟡 **Yellow**: Watch, RSI warning, Normal volume
- 🔵 **Blue**: Information, Click for details

### Recommendation Scores
- **🚀 4/4**: Strong Buy - Highly recommended
- **📈 3/4**: Buy - Good opportunity
- **👀 2/4**: Watch - Monitor closely
- **📉 1/4**: Sell - Consider exiting
- **⛔ 0/4**: Strong Sell - Avoid

### Alert Types
- **🎯 Sell Target**: Your profit target reached
- **💰 Buy Dip**: Stock dropped 15% from high
- **⛔ Stop Loss**: Your loss limit reached
- **📊 RSI Signal**: Overbought/oversold condition

---

## Sample Data

10 NEPSE stocks are pre-loaded:
1. NABIL - Nabil Bank (Banking)
2. NNPL - Nepal Noodle (Trading)
3. AKBPL - Akbari Cement (Cement)
4. CCBL - Century Commercial Bank (Banking)
5. EBL - Everest Bank (Banking)
6. GFCL - Global Finance (Finance)
7. HBL - Himalayan Bank (Banking)
8. ICFC - ICFC Finance (Finance)
9. JBBL - Janakpur Bank (Banking)
10. KBBL - Kist Bank (Banking)

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check if port 8000 is free
# If not, stop other services or run on different port:
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 16+

# Clear npm cache and try again
npm cache clean --force
npm install
npm run dev
```

### Can't connect backend to frontend
- Make sure both servers are running
- Check http://localhost:8000/health returns 200
- Check browser console for errors (F12)

### Database errors
```bash
# Delete old database
rm backend/nepse.db

# Reinitialize
curl http://localhost:8000/api/v1/stocks/initialize
```

---

## Next Steps

1. ✅ Application is running
2. 📊 Add more stocks to portfolio
3. 💡 Watch alerts and signals
4. 🎯 Backtest your trading strategy
5. 📱 Plan mobile version (future)
6. 🔐 Add user authentication (future)

---

## Need Help?

1. Check the main [README.md](../README.md)
2. Read [API.md](./API.md) for endpoint details
3. Review [DATABASE.md](./DATABASE.md) for schema info
4. Check browser console (F12) for errors

---

Happy Investing! 🚀📈💰

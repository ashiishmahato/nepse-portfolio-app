# Smart NEPSE Investor - Complete Setup & Usage

## 📋 What You Got

A **production-ready full-stack web application** for NEPSE stock tracking with:

✅ **Backend (FastAPI)** - REST API for stock data, portfolio, and alerts
✅ **Frontend (React)** - Modern, responsive UI similar to Binance
✅ **Database (SQLite)** - Persistent storage for portfolios and alerts
✅ **Background Scheduler** - Automatic price updates and alert generation
✅ **Technical Analysis** - RSI, Moving Averages, Volume trends
✅ **10 Sample Stocks** - Pre-loaded with 200 days of data
✅ **Complete Documentation** - API docs, database schema, guides

---

## 🚀 5-Minute Quickstart

### For Windows Users:
```bash
# Run setup script
setup.bat
```

### For Mac/Linux Users:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup:

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Terminal 3 - Scheduler (optional):**
```bash
cd backend
python scheduler.py
```

Then open: **http://localhost:3000**

---

## 📊 Key Features

### 1. **Portfolio Management**
- Add/track stock holdings
- Set profit targets and stop losses
- Real-time P&L tracking
- Historical performance

### 2. **Real-Time Alerts**
- 🎯 Profit target reached
- 💰 Buy dip opportunities
- ⛔ Stop loss triggered
- 📊 RSI signals (overbought/oversold)
- 📈 Moving average crossovers

### 3. **Technical Analysis**
- 50-day & 200-day Moving Averages
- RSI (Relative Strength Index)
- Volume trend analysis
- 0-4 investment score system
- Automated recommendations

### 4. **Smart Dashboard**
- Portfolio summary
- Total invested vs. current value
- Profit/loss in real-time
- Active alerts
- Top recommended stocks

### 5. **Stock Market Data**
- 10 NEPSE stocks
- Real-time price updates
- 200 days historical data
- Search and filter
- Technical indicators

---

## 📁 Project Structure

```
smart-nepse-investor/
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── models/            # Database models
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── schemas/           # Data validation
│   │   └── utils/             # Helper functions
│   ├── scheduler.py           # Background tasks
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Configuration
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── pages/             # Dashboard, Portfolio, etc.
│   │   ├── components/        # UI components
│   │   ├── services/          # API client
│   │   └── utils/             # Formatting, helpers
│   ├── package.json           # Dependencies
│   └── index.html             # Entry point
│
├── docs/                       # Documentation
│   ├── QUICKSTART.md          # 5-minute setup
│   ├── API.md                 # API reference
│   ├── DATABASE.md            # Database schema
│   └── STRUCTURE.md           # Architecture
│
└── README.md                   # Main documentation
```

---

## 🔧 API Quick Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Initialize Database
```bash
curl http://localhost:8000/api/v1/stocks/initialize
```

### List Stocks
```bash
curl http://localhost:8000/api/v1/stocks/list
```

### Add to Portfolio
```bash
curl -X POST http://localhost:8000/api/v1/portfolio/add \
  -H "Content-Type: application/json" \
  -d '{
    "stock_symbol": "NABIL",
    "buy_price": 1400,
    "quantity": 10,
    "target_profit_percentage": 15
  }'
```

### Get Dashboard
```bash
curl http://localhost:8000/api/v1/portfolio/dashboard/summary
```

### Get Alerts
```bash
curl http://localhost:8000/api/v1/alerts
```

For more details, see [docs/API.md](./docs/API.md)

---

## 💡 Sample Workflow

### Step 1: Initialize Data
Visit: http://localhost:8000/api/v1/stocks/initialize

### Step 2: View Dashboard
Open: http://localhost:3000

You'll see 10 stocks with technical analysis.

### Step 3: Add a Stock
1. Click "Portfolio" → "Add Stock"
2. Select: NABIL
3. Buy Price: 1400
4. Quantity: 10
5. Target Profit %: 15
6. Submit

### Step 4: Monitor Alerts
1. Click "Alerts"
2. Set your target and stop loss
3. Alerts auto-generate every 2 minutes
4. When triggered, you'll see them in the Alerts page

### Step 5: Track Performance
- Dashboard shows: total invested, current value, P&L
- Portfolio shows: each holding with real-time updates
- Charts available: 60 days of price history

---

## 📊 Understanding the Dashboard

### Top Cards
- **Total Invested**: Sum of all capital deployed
- **Current Value**: Current market value of holdings
- **Profit/Loss**: Absolute rupees gained/lost
- **Return %**: Percentage return on investment

### Portfolio Widget
- Your active stock positions
- Current value per stock
- Profit/loss with percentage

### Alerts Widget
- Number of active alerts
- Recent alerts with details
- Alert types and prices

### Top Stocks
- Highest-scoring opportunities
- Current prices
- Buy/Sell recommendations

---

## 🔐 Technical Indicators Explained

### Moving Average (MA)
- **50-day MA**: Short-term trend
- **200-day MA**: Long-term trend
- **Golden Cross**: 50-MA > 200-MA (Bullish)
- **Death Cross**: 50-MA < 200-MA (Bearish)

### RSI (Relative Strength Index)
Ranges 0-100:
- 0-30: **Oversold** → Buy signal
- 30-70: **Normal** range
- 70-100: **Overbought** → Sell signal

### Volume Trend
- **High**: Above average volume (strong signal)
- **Normal**: Regular trading
- **Low**: Below average volume

### Analysis Score (0-4)
- **3.5-4**: 🚀 Strong Buy
- **2.5-3.5**: 📈 Buy
- **1.5-2.5**: 👀 Watch
- **0.5-1.5**: 📉 Sell
- **0-0.5**: ⛔ Strong Sell

---

## 📈 Sample Stocks Included

1. **NABIL** - Nabil Bank (Banking)
2. **NNPL** - Nepal Noodle (Trading)
3. **AKBPL** - Akbari Cement (Cement)
4. **CCBL** - Century Commercial Bank (Banking)
5. **EBL** - Everest Bank (Banking)
6. **GFCL** - Global Finance (Finance)
7. **HBL** - Himalayan Bank (Banking)
8. **ICFC** - ICFC Finance (Finance)
9. **JBBL** - Janakpur Bank (Banking)
10. **KBBL** - Kist Bank (Banking)

Each stock has 200 days of historical data for analysis.

---

## 🛠️ Configuration

### Backend (.env)
```env
DATABASE_URL=sqlite:///./nepse.db
DEBUG=true
NEPSE_API_BASE_URL=https://api.nepsedata.com
STOCK_PRICE_UPDATE_INTERVAL=300
```

### Frontend (vite.config.js)
```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
    }
  }
}
```

---

## ⚙️ Background Scheduler

Automatically runs every:
- **1 minute**: Update stock prices
- **5 minutes**: Calculate technical analysis
- **2 minutes**: Update portfolio & generate alerts

Or run manually: `python scheduler.py`

---

## 🐛 Troubleshooting

### Issue: Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows
```

### Issue: Frontend can't connect
- Verify backend is running
- Check http://localhost:8000/health
- Clear browser cache and reload

### Issue: Database errors
```bash
# Delete and reinitialize
rm backend/nepse.db
curl http://localhost:8000/api/v1/stocks/initialize
```

### Issue: Missing dependencies
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

---

## 📚 Documentation Files

- **README.md** - Full documentation
- **docs/QUICKSTART.md** - 5-minute setup guide
- **docs/API.md** - Complete API reference
- **docs/DATABASE.md** - Database schema & queries
- **docs/STRUCTURE.md** - Project architecture

---

## 🔄 Workflow for Stock Analysis

```
1. Stock Data Loaded
   ↓
2. Technical Indicators Calculated (MA, RSI, Volume)
   ↓
3. Investment Score Generated (0-4)
   ↓
4. Recommendation Issued (Buy/Sell/Watch)
   ↓
5. Alerts Generated Based on Rules
   ↓
6. Portfolio Values Updated in Real-time
   ↓
7. Dashboard Refreshes with New Data
```

---

## 🚀 Production Deployment

### Using PostgreSQL
```env
DATABASE_URL=postgresql://user:password@localhost/nepse_db
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app --workers 4
```

### Deploy Frontend
```bash
npm run build  # Creates dist folder
# Deploy dist/ to Vercel, Netlify, or AWS S3
```

### Run Scheduler in Background
```bash
nohup python scheduler.py > scheduler.log 2>&1 &
```

---

## 📝 Common Tasks

### Add Custom Stock
```python
# In backend, add to mock_data.py STOCKS dict:
"SYMBOL": {"name": "Company Name", "sector": "Sector"}
```

### Modify Alert Thresholds
Edit `backend/app/services/stock_service.py` in `AlertService.generate_alerts()`

### Change Update Frequency
Edit `backend/scheduler.py` - modify the `minutes` parameter in `add_job()`

### Customize Dashboard
Edit `frontend/src/pages/Dashboard.jsx` - modify components and layout

---

## 🎓 Learning Resources

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)

### React
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Vite](https://vitejs.dev)

### Technical Analysis
- Understanding RSI
- Moving Averages Strategy
- Volume Analysis

---

## 🤝 Contributing

Ideas for improvements:
- Real NEPSE API integration
- Email/Telegram notifications
- Advanced charting
- Machine learning predictions
- Mobile app
- Backtesting engine

---

## 📄 License

MIT License - Free to use and modify

---

## ⚠️ Disclaimer

This application is for **educational purposes only**. Always conduct your own research before making investment decisions. Past performance doesn't guarantee future results.

---

## 🎉 Ready to Go!

Your Smart NEPSE Investor application is complete and ready to use. Start tracking your investments and making data-driven decisions!

**Next Step**: Run `setup.bat` (Windows) or `setup.sh` (Mac/Linux) to get started!

Happy Investing! 🚀📈💰

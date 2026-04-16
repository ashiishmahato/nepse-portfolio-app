# Smart NEPSE Investor

A full-stack web application for personal stock tracking and alert system for Nepal Stock Exchange (NEPSE). Make smart investment decisions with real-time price tracking, technical analysis, and intelligent alerts.

## Features

### 🎯 Core Features

1. **User Portfolio Management**
   - Add stocks with buy price, quantity, and target profit percentage
   - Track stop loss levels
   - View profit/loss in real-time
   - Manage multiple positions

2. **Real-Time Price Tracking**
   - Live stock prices updated every minute
   - Historical price data for technical analysis
   - Price charts with 60+ days of data

3. **Intelligent Alert System**
   - **Profit Target Alerts**: Notify when price reaches your profit target
   - **Buy Dip Alerts**: Alert when price drops 15% from recent high
   - **Stop Loss Alerts**: Trigger when price hits your stop loss
   - **RSI Signals**: Technical indicators-based alerts
   - **Moving Average Crossovers**: MA-based trading signals

4. **Technical Analysis**
   - **Moving Averages**: 50-day and 200-day MAs
   - **RSI (Relative Strength Index)**: Overbought/oversold detection
   - **Volume Trend**: High/normal/low volume analysis
   - **Investment Score**: 0-4 scale recommendation system

5. **Professional Dashboard**
   - Portfolio summary and performance metrics
   - Active alerts overview
   - Top recommended stocks
   - Real-time profit/loss tracking

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: React 18 with Vite
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Charts**: Chart.js
- **UI**: Tailwind CSS
- **Scheduling**: APScheduler

## Project Structure

```
smart-nepse-investor/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utilities & mock data
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── main.py          # FastAPI app
│   ├── scheduler.py         # Background tasks
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service
│   │   ├── utils/           # Utilities
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
│
├── docs/                    # Documentation
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend folder**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (Optional but recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database** (Optional - happens automatically on first run)
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

5. **Run the FastAPI server**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   
   Server will run at: `http://localhost:8000`
   API docs available at: `http://localhost:8000/docs`

6. **In another terminal, run the background scheduler** (for automatic price updates)
   ```bash
   python scheduler.py
   ```

### Frontend Setup

1. **Navigate to frontend folder**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   Frontend will run at: `http://localhost:3000`

## Usage Guide

### Getting Started

1. **Initialize Database**
   - Visit: `http://localhost:8000/api/v1/stocks/initialize`
   - This loads 10 sample NEPSE stocks with 200 days of historical data

2. **Access Dashboard**
   - Open: `http://localhost:3000`
   - View your investment overview

3. **Add Stocks to Portfolio**
   - Go to Portfolio page
   - Click "Add Stock" button
   - Select stock symbol, buy price, quantity
   - Set target profit % and optional stop loss %
   - Submit

4. **Monitor Alerts**
   - Check Alerts page for generated alerts
   - Alerts are generated automatically every 2 minutes
   - Mark alerts as read when addressed

### Dashboard Overview

**Top Cards Show:**
- Total Invested: Sum of all investments
- Current Value: Current portfolio worth
- Profit/Loss: Absolute gain/loss in rupees
- Return %: Percentage return on investment

**Portfolio Holdings:**
- Your active stock positions
- Current value per position
- Profit/loss percentage

**Active Alerts:**
- Number of active alerts
- Recent alert list
- Alert types and details

**Top Recommended Stocks:**
- Stocks with highest analysis scores
- Current price
- Recommendation (Strong Buy, Buy, Watch, etc.)

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Stocks Endpoints

#### Initialize Database
```
GET /stocks/initialize
```

#### List All Stocks
```
GET /stocks/list
```

Response:
```json
[
  {
    "symbol": "NABIL",
    "name": "Nabil Bank Limited",
    "sector": "Banking",
    "current_price": 1450.00,
    "ma_50": 1420.30,
    "ma_200": 1380.50,
    "rsi": 65.5,
    "analysis_score": 3.2,
    "analysis_recommendation": "buy"
  }
]
```

#### Get Stock Details
```
GET /stocks/{symbol}
```

#### Get Price History
```
GET /stocks/{symbol}/history?days=60
```

#### Get Technical Analysis
```
GET /stocks/{symbol}/technical-analysis
```

### Portfolio Endpoints

#### Add to Portfolio
```
POST /portfolio/add
```

Request Body:
```json
{
  "stock_symbol": "NABIL",
  "buy_price": 1400.0,
  "quantity": 10,
  "target_profit_percentage": 15.0,
  "stop_loss_percentage": 10.0,
  "notes": "Long-term hold"
}
```

#### Get Portfolio List
```
GET /portfolio/list
```

#### Get Dashboard Summary
```
GET /portfolio/dashboard/summary
```

#### Update Portfolio Item
```
PUT /portfolio/{id}
```

#### Remove from Portfolio
```
DELETE /portfolio/{id}
```

### Alerts Endpoints

#### Get All Alerts
```
GET /alerts/?active_only=true&limit=50
```

#### Generate Alerts
```
POST /alerts/generate
```

#### Mark Alert as Read
```
PUT /alerts/{id}/mark-as-read
```

#### Deactivate Alert
```
PUT /alerts/{id}/deactivate
```

## Configuration

Edit `.env` file in backend folder:

```env
# Database
DATABASE_URL=sqlite:///./nepse.db

# API Settings
NEPSE_API_BASE_URL=https://api.nepsedata.com
STOCK_PRICE_UPDATE_INTERVAL=300

# Notifications (Optional)
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_CHAT_ID=your-chat-id
ENABLE_EMAIL_ALERTS=false

# Debug
DEBUG=true
```

## Sample Data

10 NEPSE stocks are included with mock data:

1. **NABIL** - Nabil Bank Limited (Banking)
2. **NNPL** - Nepal Noodle PVT LTD (Trading)
3. **AKBPL** - Akbari Cement Limited (Cement)
4. **CCBL** - Century Commercial Bank (Banking)
5. **EBL** - Everest Bank Limited (Banking)
6. **GFCL** - Global Finance Limited (Finance)
7. **HBL** - Himalayan Bank Limited (Banking)
8. **ICFC** - ICFC Finance Limited (Finance)
9. **JBBL** - Janakpur Bank Limited (Banking)
10. **KBBL** - Kist Bank Limited (Banking)

To load sample data:
```bash
# Call the initialize endpoint from browser or curl
curl http://localhost:8000/api/v1/stocks/initialize
```

## Technical Indicators Explained

### Moving Average (MA)
- **50-day MA**: Short-term trend indicator
- **200-day MA**: Long-term trend indicator
- **Golden Cross**: When 50-MA crosses above 200-MA (Bullish)
- **Death Cross**: When 50-MA crosses below 200-MA (Bearish)

### RSI (Relative Strength Index)
- **0-30**: Oversold (potential buying opportunity)
- **30-70**: Normal range
- **70-100**: Overbought (potential selling opportunity)

### Volume Trend
- **High**: Above average volume (strength signal)
- **Normal**: Normal trading volume
- **Low**: Below average volume

### Analysis Score (0-4)
- **3.5-4**: Strong Buy 🚀
- **2.5-3.5**: Buy 📈
- **1.5-2.5**: Watch 👀
- **0.5-1.5**: Sell 📉
- **0-0.5**: Strong Sell ⛔

## Background Tasks

The scheduler automatically:

1. **Updates stock prices** (Every 1 minute)
2. **Calculates technical analysis** (Every 5 minutes)
3. **Updates portfolio values** (Every 2 minutes)
4. **Generates alerts** (Every 2 minutes)
5. **Deactivates old alerts** (Every 2 minutes)

## Production Deployment

### Backend Deployment

1. **Use PostgreSQL instead of SQLite**
   ```env
   DATABASE_URL=postgresql://user:password@localhost/nepse_db
   ```

2. **Install PostgreSQL driver**
   ```bash
   pip install psycopg2-binary
   ```

3. **Deploy with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

4. **Run scheduler separately**
   ```bash
   python scheduler.py &
   ```

### Frontend Deployment

1. **Build for production**
   ```bash
   npm run build
   ```

2. **Deploy to Vercel, Netlify, or any static host**

## Future Enhancements

- [ ] Email & Telegram notifications
- [ ] User authentication & multiple portfolios
- [ ] Advanced charting with candlesticks
- [ ] Comparative analysis between stocks
- [ ] Historical performance tracking
- [ ] Export portfolio reports (PDF/CSV)
- [ ] Mobile app (React Native)
- [ ] Integration with real NEPSE API
- [ ] Backtesting tools
- [ ] Machine learning predictions

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process and restart
```

### Frontend can't connect to backend
- Check if backend server is running on `http://localhost:8000`
- Check CORS settings in `backend/app/main.py`
- Verify proxy settings in `frontend/vite.config.js`

### Database errors
```bash
# Delete old database and reinitialize
rm backend/nepse.db

# Then call initialize endpoint:
curl http://localhost:8000/api/v1/stocks/initialize
```

## Support & Contribution

For issues, questions, or suggestions:
1. Check existing documentation
2. Review sample data initialization
3. Check console logs for errors

## License

MIT License - Feel free to use and modify as needed

## Disclaimer

This application is for educational purposes. Always do your own research before making investment decisions. Past performance doesn't guarantee future results.

---

Happy Investing! 📈💰

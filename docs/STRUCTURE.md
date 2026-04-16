# Project Structure and File Descriptions

## Backend Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py         # Model exports
│   │   ├── stock.py            # Stock model
│   │   ├── portfolio.py        # Portfolio model
│   │   ├── price_history.py    # Price history model
│   │   └── alert.py            # Alert model
│   ├── routes/
│   │   ├── __init__.py         # Route exports
│   │   ├── stocks.py           # Stock endpoints
│   │   ├── portfolio.py        # Portfolio endpoints
│   │   └── alerts.py           # Alert endpoints
│   ├── schemas/
│   │   └── __init__.py         # Pydantic schemas for validation
│   ├── services/
│   │   ├── __init__.py         # Service exports
│   │   ├── technical_analysis.py   # TA calculations
│   │   ├── stock_service.py    # Stock management
│   │   └── notifications.py    # Future: Email/Telegram
│   ├── utils/
│   │   ├── __init__.py         # Utilities exports
│   │   └── mock_data.py        # Mock NEPSE data provider
│   ├── config.py               # Configuration & settings
│   ├── database.py             # SQLAlchemy setup
│   └── main.py                 # FastAPI application
├── scheduler.py                # Background tasks
├── requirements.txt            # Python dependencies
├── .env                        # Environment config
└── .gitignore                  # Git ignore rules
```

## Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Navigation & layout
│   │   └── common.jsx          # Shared UI components
│   ├── pages/
│   │   ├── Dashboard.jsx       # Dashboard page
│   │   ├── Portfolio.jsx       # Portfolio page
│   │   ├── Stocks.jsx          # Stocks listing
│   │   └── Alerts.jsx          # Alerts page
│   ├── services/
│   │   └── api.js              # API client
│   ├── utils/
│   │   └── formatting.js       # Formatting utilities
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # React entry point
│   └── index.css               # Global styles
├── index.html                  # HTML template
├── package.json                # Dependencies
├── vite.config.js              # Vite config
├── tailwind.config.js          # Tailwind config
├── postcss.config.js           # PostCSS config
└── .gitignore                  # Git ignore rules
```

## Database Schema

### stocks table
- symbol (string, PK): NABIL, NNPL, etc.
- name (string): Full name
- sector (string): Industry sector
- current_price (float): Market price
- ma_50, ma_200 (float): Moving averages
- rsi (float): RSI indicator
- analysis_score (float): 0-4
- analysis_recommendation (string): Buy/Sell/Watch

### portfolio table
- id (integer, PK): Auto-increment
- stock_symbol (string, FK): Reference to stock
- buy_price (float): Entry price
- quantity (integer): Number of shares
- target_profit_percentage (float): Profit target
- stop_loss_percentage (float): Loss limit
- total_invested (float): Cost basis
- current_value (float): Market value
- profit_loss (float): Absolute P&L

### price_history table
- id (integer, PK): Auto-increment
- stock_symbol (string, FK): Stock reference
- date (datetime): Trading date
- open_price, high_price, low_price, close_price (float): OHLC
- volume (integer): Trading volume

### alerts table
- id (integer, PK): Auto-increment
- stock_symbol (string, FK): Stock reference
- alert_type (string): sell_target, buy_dip, stop_loss, etc.
- title (string): Alert title
- description (string): Alert description
- current_price (float): Price when created
- trigger_price (float): Target price
- is_active (boolean): Active status
- is_notified (boolean): Notified status

## API Endpoints

### Stocks
- GET /stocks/initialize - Initialize database
- GET /stocks/list - List all stocks
- GET /stocks/{symbol} - Get stock details
- GET /stocks/search - Search stocks
- GET /stocks/{symbol}/history - Price history
- GET /stocks/{symbol}/technical-analysis - TA data

### Portfolio
- POST /portfolio/add - Add stock
- GET /portfolio/list - Get holdings
- GET /portfolio/{id} - Get item details
- PUT /portfolio/{id} - Update item
- DELETE /portfolio/{id} - Remove item
- GET /portfolio/dashboard/summary - Dashboard data

### Alerts
- GET /alerts - Get all alerts
- GET /alerts/by-stock/{symbol} - Stock alerts
- GET /alerts/{id} - Alert details
- PUT /alerts/{id}/mark-as-read - Mark as read
- PUT /alerts/{id}/deactivate - Deactivate
- POST /alerts/generate - Generate alerts

## Key Features Implementation

### Technical Analysis Engine
- RSI: Measures overbought (>70) and oversold (<30)
- Moving Averages: 50-day and 200-day trends
- Volume Trend: High/normal/low analysis
- Score Calculation: 0-4 scale for recommendations

### Alert System
- Profit Target: When price ≥ target
- Buy Dip: When price drops 15% from high
- Stop Loss: When price hits loss limit
- RSI Signals: Overbought/oversold alerts
- Automatic deactivation of old alerts

### Mock Data
- 10 NEPSE stocks pre-loaded
- 200 days of historical data per stock
- Realistic price variations
- Volume data for analysis

## Configuration Files

### .env (Backend)
- DATABASE_URL: SQLite or PostgreSQL
- NEPSE_API_BASE_URL: API endpoint
- TELEGRAM_BOT_TOKEN: For notifications
- DEBUG: Development mode

### vite.config.js (Frontend)
- API proxy to backend
- Port 3000 for development
- HMR for hot reload

### tailwind.config.js (Frontend)
- Custom colors (primary, secondary)
- Dark theme colors
- Responsive breakpoints

## Development Workflow

1. **Backend Development**
   - Add new models in models/
   - Create schemas in schemas/
   - Implement routes in routes/
   - Add business logic in services/

2. **Frontend Development**
   - Create components in components/
   - Build pages in pages/
   - Update formatting utils
   - Add API calls in services/api.js

3. **Testing**
   - Test API endpoints in /docs
   - Try UI components manually
   - Verify database operations
   - Check scheduler logs

## Deployment Checklist

- [ ] Set DEBUG=false
- [ ] Update SECRET_KEY
- [ ] Configure production database
- [ ] Set up CORS properly
- [ ] Enable HTTPS
- [ ] Configure email/Telegram notifications
- [ ] Set up monitoring
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting

## Performance Optimization

- Database indexes on frequently queried columns
- API response caching
- Lazy loading of price history
- Pagination for large datasets
- Optional: Redis caching layer

## Future Enhancements

- Real NEPSE API integration
- User authentication & multi-portfolio support
- Advanced charting (candlesticks, Bollinger Bands)
- Machine learning predictions
- Mobile app (React Native)
- Backtesting engine
- Export functionality (PDF, CSV)
- Social features (share portfolios)

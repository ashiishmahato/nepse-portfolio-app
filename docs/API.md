# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API doesn't require authentication. In production, implement JWT tokens.

---

## Stocks API

### Initialize Database
Populates database with sample NEPSE stocks and historical data.

**Endpoint:** `GET /stocks/initialize`

**Response:**
```json
{
  "message": "Database initialized successfully",
  "stocks_added": 10,
  "historical_data_days": 200
}
```

---

### List All Stocks
Get list of all stocks with current prices and analysis.

**Endpoint:** `GET /stocks/list`

**Response:**
```json
[
  {
    "symbol": "NABIL",
    "name": "Nabil Bank Limited",
    "sector": "Banking",
    "current_price": 1450.25,
    "ma_50": 1420.30,
    "ma_200": 1380.50,
    "rsi": 65.5,
    "analysis_score": 3.2,
    "analysis_recommendation": "buy",
    "volume_trend": "high",
    "recent_high": 1480.00,
    "high_52w": 1500.00,
    "low_52w": 1200.00,
    "last_update": "2024-04-15T10:30:00"
  }
]
```

---

### Get Stock Details
Get detailed information for a specific stock.

**Endpoint:** `GET /stocks/{symbol}`

**Path Parameters:**
- `symbol` (string): Stock symbol (e.g., NABIL)

**Response:**
```json
{
  "symbol": "NABIL",
  "name": "Nabil Bank Limited",
  "sector": "Banking",
  "current_price": 1450.25,
  "ma_50": 1420.30,
  "ma_200": 1380.50,
  "rsi": 65.5,
  "analysis_score": 3.2,
  "analysis_recommendation": "buy",
  "volume_trend": "high",
  "recent_high": 1480.00,
  "high_52w": 1500.00,
  "low_52w": 1200.00,
  "last_update": "2024-04-15T10:30:00"
}
```

---

### Search Stocks
Search stocks by symbol, name, or sector.

**Endpoint:** `GET /stocks/search`

**Query Parameters:**
- `query` (string): Search term

**Response:**
```json
[
  {
    "symbol": "NABIL",
    "name": "Nabil Bank Limited",
    "sector": "Banking",
    "current_price": 1450.25
  }
]
```

---

### Get Price History
Get historical price data for charting (for last N days).

**Endpoint:** `GET /stocks/{symbol}/history`

**Query Parameters:**
- `days` (integer, default: 60): Number of days of history

**Response:**
```json
[
  {
    "date": "2024-03-15T00:00:00",
    "open": 1420.00,
    "high": 1450.00,
    "low": 1410.00,
    "close": 1445.00,
    "volume": 250000
  }
]
```

---

### Get Technical Analysis
Get technical analysis indicators for a stock.

**Endpoint:** `GET /stocks/{symbol}/technical-analysis`

**Response:**
```json
{
  "symbol": "NABIL",
  "name": "Nabil Bank Limited",
  "current_price": 1450.25,
  "ma_50": 1420.30,
  "ma_200": 1380.50,
  "rsi": 65.5,
  "volume_trend": "high",
  "analysis_score": 3.2,
  "recommendation": "buy",
  "high_52w": 1500.00,
  "low_52w": 1200.00,
  "recent_high": 1480.00
}
```

---

### Update Stock Prices
Manually trigger price update (called by scheduler).

**Endpoint:** `POST /stocks/update-prices`

**Response:**
```json
{
  "message": "Updated prices for 10 stocks"
}
```

---

## Portfolio API

### Add Stock to Portfolio
Add a stock to your portfolio.

**Endpoint:** `POST /portfolio/add`

**Request Body:**
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

**Response:**
```json
{
  "id": 1,
  "stock_symbol": "NABIL",
  "buy_price": 1400.0,
  "quantity": 10,
  "target_profit_percentage": 15.0,
  "stop_loss_percentage": 10.0,
  "total_invested": 14000.0,
  "current_value": 14502.5,
  "profit_loss": 502.5,
  "profit_loss_percentage": 3.59,
  "is_sold": 0,
  "sell_price": null,
  "purchase_date": "2024-04-15T10:30:00",
  "notes": "Long-term hold"
}
```

---

### Get Portfolio List
Get all portfolio holdings.

**Endpoint:** `GET /portfolio/list`

**Query Parameters:**
- `include_sold` (boolean, default: false): Include sold positions

**Response:**
```json
[
  {
    "id": 1,
    "stock_symbol": "NABIL",
    "buy_price": 1400.0,
    "quantity": 10,
    "target_profit_percentage": 15.0,
    "stop_loss_percentage": 10.0,
    "total_invested": 14000.0,
    "current_value": 14502.5,
    "profit_loss": 502.5,
    "profit_loss_percentage": 3.59,
    "is_sold": 0
  }
]
```

---

### Get Portfolio Item
Get specific portfolio holding details.

**Endpoint:** `GET /portfolio/{id}`

**Path Parameters:**
- `id` (integer): Portfolio item ID

**Response:**
```json
{
  "id": 1,
  "stock_symbol": "NABIL",
  "buy_price": 1400.0,
  "quantity": 10,
  "target_profit_percentage": 15.0,
  "stop_loss_percentage": 10.0,
  "total_invested": 14000.0,
  "current_value": 14502.5,
  "profit_loss": 502.5,
  "profit_loss_percentage": 3.59,
  "is_sold": 0
}
```

---

### Update Portfolio Item
Update portfolio holding details.

**Endpoint:** `PUT /portfolio/{id}`

**Request Body:**
```json
{
  "target_profit_percentage": 20.0,
  "stop_loss_percentage": 8.0,
  "notes": "Adjusted targets"
}
```

**Response:**
```json
{
  "id": 1,
  "stock_symbol": "NABIL",
  "target_profit_percentage": 20.0,
  "stop_loss_percentage": 8.0,
  "notes": "Adjusted targets"
}
```

---

### Remove from Portfolio
Mark portfolio holding as sold.

**Endpoint:** `DELETE /portfolio/{id}`

**Response:**
```json
{
  "message": "Item removed from portfolio",
  "portfolio_id": 1
}
```

---

### Get Dashboard Summary
Get complete portfolio summary with stats and alerts.

**Endpoint:** `GET /portfolio/dashboard/summary`

**Response:**
```json
{
  "total_invested": 14000.0,
  "total_current_value": 14502.5,
  "total_profit_loss": 502.5,
  "total_profit_loss_percentage": 3.59,
  "portfolio_count": 1,
  "active_alerts_count": 2,
  "portfolio_items": [...],
  "recent_alerts": [...]
}
```

---

## Alerts API

### Get All Alerts
Get list of alerts (active or all).

**Endpoint:** `GET /alerts/`

**Query Parameters:**
- `active_only` (boolean, default: true): Show only active alerts
- `limit` (integer, default: 50): Maximum alerts to return

**Response:**
```json
[
  {
    "id": 1,
    "stock_symbol": "NABIL",
    "alert_type": "sell_target",
    "title": "🎯 Sell Target Reached: NABIL",
    "description": "Your target profit of 15% has been reached!",
    "current_price": 1610.0,
    "trigger_price": 1610.0,
    "is_active": 1,
    "is_notified": 0,
    "created_at": "2024-04-15T10:30:00",
    "notified_at": null
  }
]
```

---

### Get Alerts by Stock
Get alerts for a specific stock.

**Endpoint:** `GET /alerts/by-stock/{symbol}`

**Query Parameters:**
- `active_only` (boolean, default: true): Show only active alerts

**Response:**
```json
[
  {
    "id": 1,
    "stock_symbol": "NABIL",
    "alert_type": "sell_target",
    "title": "🎯 Sell Target Reached: NABIL",
    "description": "Your target profit of 15% has been reached!",
    "current_price": 1610.0,
    "trigger_price": 1610.0,
    "is_active": 1,
    "is_notified": 0,
    "created_at": "2024-04-15T10:30:00"
  }
]
```

---

### Get Alert Details
Get specific alert information.

**Endpoint:** `GET /alerts/{id}`

**Path Parameters:**
- `id` (integer): Alert ID

**Response:**
```json
{
  "id": 1,
  "stock_symbol": "NABIL",
  "alert_type": "sell_target",
  "title": "🎯 Sell Target Reached: NABIL",
  "description": "Your target profit of 15% has been reached!",
  "current_price": 1610.0,
  "trigger_price": 1610.0,
  "is_active": 1,
  "is_notified": 0,
  "created_at": "2024-04-15T10:30:00",
  "notified_at": null
}
```

---

### Mark Alert as Read
Mark an alert as notified.

**Endpoint:** `PUT /alerts/{id}/mark-as-read`

**Response:**
```json
{
  "message": "Alert marked as read"
}
```

---

### Deactivate Alert
Mark an alert as inactive.

**Endpoint:** `PUT /alerts/{id}/deactivate`

**Response:**
```json
{
  "message": "Alert deactivated"
}
```

---

### Generate Alerts
Manually trigger alert generation (called by scheduler).

**Endpoint:** `POST /alerts/generate`

**Response:**
```json
{
  "message": "Alerts generated successfully"
}
```

---

## Alert Types

### Sell Target Alert
Triggered when: `current_price >= buy_price × (1 + target_profit_percentage%)`

Example:
- Bought at: 1000
- Target profit: 15%
- Trigger price: 1150

### Buy Dip Alert
Triggered when: `current_price <= recent_high × 0.85` (15% drop from recent high)

Example:
- Recent high: 1500
- Dip threshold: 1275
- Triggered at: 1275 or below

### Stop Loss Alert
Triggered when: `current_price <= buy_price × (1 - stop_loss_percentage%)`

Example:
- Bought at: 1000
- Stop loss: 10%
- Trigger price: 900

### RSI Signal
Triggered when: `RSI > 70` (overbought) or `RSI < 30` (oversold)

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limits

Currently no rate limits. In production, implement:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## Changelog

### v1.0.0 (2024-04-15)
- Initial release
- Stock tracking
- Portfolio management
- Alert system
- Technical analysis

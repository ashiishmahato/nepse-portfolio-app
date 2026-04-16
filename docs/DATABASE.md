# Database Schema

## Overview

Smart NEPSE Investor uses SQLite for data persistence. The database consists of 4 main tables:

1. **stocks** - Stock master data
2. **portfolio** - User's stock holdings
3. **price_history** - Historical price data
4. **alerts** - Generated alerts

---

## Table: stocks

Stores stock information and current technical analysis.

```sql
CREATE TABLE stocks (
    symbol VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    sector VARCHAR,
    current_price FLOAT DEFAULT 0.0,
    last_update DATETIME,
    
    -- Technical Analysis
    ma_50 FLOAT,                    -- 50-day moving average
    ma_200 FLOAT,                   -- 200-day moving average
    rsi FLOAT,                      -- Relative Strength Index
    volume_trend VARCHAR,           -- high, normal, low
    
    -- Analysis Score
    analysis_score FLOAT DEFAULT 0.0,
    analysis_recommendation VARCHAR,
    
    -- Historical Data
    high_52w FLOAT,
    low_52w FLOAT,
    recent_high FLOAT
);
```

### Fields
- **symbol** (PK): Stock symbol (NABIL, NNPL, etc.)
- **name**: Full stock name
- **sector**: Industry sector
- **current_price**: Latest market price
- **ma_50/200**: Moving averages for trend analysis
- **rsi**: Oscillator ranging 0-100
- **volume_trend**: Trading volume analysis
- **analysis_score**: 0-4 investment score
- **analysis_recommendation**: Buy/Sell/Watch signal
- **high_52w/low_52w**: 52-week price extremes
- **recent_high**: Recent peak price

### Indexes
```sql
CREATE INDEX idx_symbol ON stocks(symbol);
CREATE INDEX idx_analysis_score ON stocks(analysis_score);
```

---

## Table: portfolio

Tracks user's stock holdings and performance.

```sql
CREATE TABLE portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_symbol VARCHAR,           -- FK to stocks.symbol
    buy_price FLOAT,                -- Purchase price per share
    quantity INTEGER,               -- Number of shares
    target_profit_percentage FLOAT, -- Target profit %
    stop_loss_percentage FLOAT,     -- Stop loss % (optional)
    purchase_date DATETIME,
    notes VARCHAR,
    
    -- Calculated Fields
    total_invested FLOAT,           -- buy_price × quantity
    current_value FLOAT,            -- current_price × quantity
    profit_loss FLOAT,              -- current_value - total_invested
    profit_loss_percentage FLOAT,   -- (profit_loss / total_invested) × 100
    
    -- Status
    is_sold INTEGER DEFAULT 0,      -- 0=holding, 1=sold
    sell_price FLOAT,
    sell_date DATETIME,
    
    created_at DATETIME,
    updated_at DATETIME
);
```

### Fields
- **id**: Primary key
- **stock_symbol**: Reference to stock
- **buy_price**: Entry price per share
- **quantity**: Number of shares held
- **target_profit_percentage**: Exit target (%)
- **stop_loss_percentage**: Loss limit (%)
- **total_invested**: Total capital deployed
- **current_value**: Current market value
- **profit_loss**: Absolute P&L
- **profit_loss_percentage**: P&L percentage
- **is_sold**: Position status

### Indexes
```sql
CREATE INDEX idx_stock_symbol ON portfolio(stock_symbol);
CREATE INDEX idx_is_sold ON portfolio(is_sold);
CREATE INDEX idx_purchase_date ON portfolio(purchase_date);
```

### Sample Data
```sql
INSERT INTO portfolio (stock_symbol, buy_price, quantity, target_profit_percentage, stop_loss_percentage, total_invested, current_value, purchase_date)
VALUES ('NABIL', 1400.0, 10, 15.0, 10.0, 14000.0, 14500.0, '2024-04-15');
```

---

## Table: price_history

Stores daily OHLCV (Open, High, Low, Close, Volume) data.

```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_symbol VARCHAR,           -- FK to stocks.symbol
    date DATETIME,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume INTEGER
);
```

### Fields
- **id**: Primary key
- **stock_symbol**: Stock reference
- **date**: Trading date
- **open_price**: Open price
- **high_price**: High price
- **low_price**: Low price
- **close_price**: Close price
- **volume**: Trading volume

### Indexes
```sql
CREATE INDEX idx_stock_symbol_date ON price_history(stock_symbol, date);
CREATE INDEX idx_date ON price_history(date);
```

### Sample Data
```sql
INSERT INTO price_history (stock_symbol, date, open_price, high_price, low_price, close_price, volume)
VALUES ('NABIL', '2024-04-15', 1430.0, 1450.0, 1420.0, 1445.0, 250000);
```

---

## Table: alerts

Stores generated trading alerts.

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_symbol VARCHAR,           -- FK to stocks.symbol
    alert_type VARCHAR,             -- sell_target, buy_dip, stop_loss, rsi_signal
    title VARCHAR,
    description VARCHAR,
    current_price FLOAT,
    trigger_price FLOAT,
    
    -- Status
    is_active INTEGER DEFAULT 1,    -- 1=active, 0=inactive
    is_notified INTEGER DEFAULT 0,  -- 1=notified, 0=pending
    
    created_at DATETIME,
    notified_at DATETIME
);
```

### Fields
- **id**: Primary key
- **stock_symbol**: Stock reference
- **alert_type**: Type of alert (profit target, dip, stop loss, etc.)
- **title**: Alert title with emoji
- **description**: Detailed alert message
- **current_price**: Price when alert was created
- **trigger_price**: Target price that triggered alert
- **is_active**: Alert status
- **is_notified**: Notification status

### Alert Types
| Type | Trigger Condition |
|------|-------------------|
| sell_target | Price ≥ Target profit level |
| buy_dip | Price ≤ Recent high × 85% |
| stop_loss | Price ≤ Buy price × (1 - stop_loss%) |
| rsi_signal | RSI > 70 or < 30 |
| ma_crossover | Moving average crossover |

### Indexes
```sql
CREATE INDEX idx_stock_symbol ON alerts(stock_symbol);
CREATE INDEX idx_alert_type ON alerts(alert_type);
CREATE INDEX idx_is_active ON alerts(is_active);
CREATE INDEX idx_created_at ON alerts(created_at);
```

### Sample Data
```sql
INSERT INTO alerts (stock_symbol, alert_type, title, description, current_price, trigger_price, is_active)
VALUES ('NABIL', 'sell_target', '🎯 Sell Target Reached: NABIL', 'Your target profit of 15% has been reached!', 1610.0, 1610.0, 1);
```

---

## Entity Relationships

```
stocks (1) ──── (Many) portfolio
  ↓
  │
  └─────────────────────────────┐
                                ↓
                          price_history


stocks (1) ──── (Many) alerts
```

---

## Data Integrity

### Foreign Key Constraints
```sql
-- Not enforced in SQLite by default, but logically:
portfolio.stock_symbol → stocks.symbol
price_history.stock_symbol → stocks.symbol
alerts.stock_symbol → stocks.symbol
```

To enable FK constraints:
```sql
PRAGMA foreign_keys = ON;
```

---

## Migration to PostgreSQL

For production, migrate to PostgreSQL:

```sql
-- Create database
CREATE DATABASE nepse_db;

-- Create tables (same schema as above)
-- PostgreSQL will automatically handle data types and constraints better
```

Change connection string:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/nepse_db
```

---

## Database Maintenance

### Backup
```bash
# SQLite
sqlite3 nepse.db ".dump" > backup.sql

# Restore
sqlite3 nepse.db < backup.sql
```

### Cleanup
```sql
-- Delete old alerts (older than 30 days)
DELETE FROM alerts WHERE created_at < datetime('now', '-30 days');

-- Delete price history older than 2 years (optional for size)
DELETE FROM price_history WHERE date < date('now', '-2 years');
```

### Vacuum (optimize database size)
```sql
VACUUM;
```

---

## Performance Tips

1. **Indexes** are crucial for:
   - Stock lookup by symbol
   - Portfolio filtering by is_sold
   - Alert filtering by alert_type

2. **Query Optimization**:
   ```sql
   -- Good: Use indexed columns
   SELECT * FROM portfolio WHERE stock_symbol = 'NABIL';
   
   -- Bad: Avoid full table scans
   SELECT * FROM portfolio WHERE profit_loss > 0;
   ```

3. **Archiving**:
   - Archive old portfolio items (is_sold = 1)
   - Keep last 2 years of price history
   - Delete old alerts periodically

---

## Sample Queries

### Get portfolio performance
```sql
SELECT 
    stock_symbol,
    SUM(total_invested) as total_invested,
    SUM(current_value) as current_value,
    SUM(profit_loss) as profit_loss,
    (SUM(profit_loss) / SUM(total_invested) * 100) as profit_loss_pct
FROM portfolio
WHERE is_sold = 0
GROUP BY stock_symbol;
```

### Get active alerts
```sql
SELECT * FROM alerts
WHERE is_active = 1 AND stock_symbol = 'NABIL'
ORDER BY created_at DESC
LIMIT 10;
```

### Get recent price history
```sql
SELECT * FROM price_history
WHERE stock_symbol = 'NABIL'
  AND date >= date('now', '-60 days')
ORDER BY date DESC;
```

### Get stocks by recommendation
```sql
SELECT symbol, name, current_price, analysis_recommendation, analysis_score
FROM stocks
WHERE analysis_recommendation IN ('strong_buy', 'buy')
ORDER BY analysis_score DESC;
```

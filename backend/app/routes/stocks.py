"""
API routes for stock management
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import StockResponse, StockCreate, StockUpdate
from app.models import Stock, PriceHistory
from app.services.stock_service import StockService
from app.services.nepse_data_service import NepseDataService
from app.utils.mock_data import MockNEPSEDataProvider
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/initialize")
def initialize_stocks(db: Session = Depends(get_db)):
    """
    Initialize database with ALL real NEPSE stocks from NepseAPI-Unofficial
    Fetches all available stocks from https://nepseapi.surajrimal.dev
    Call this once to populate the database with all real NEPSE stocks
    """
    try:
        # Check if stocks already exist
        existing_count = db.query(Stock).count()
        if existing_count > 50:
            return {
                "message": f"Database already has {existing_count} NEPSE stocks",
                "stocks": existing_count,
                "note": "To refresh data, restart the app"
            }
        
        # Clear existing stocks to refresh
        print(f"Clearing {existing_count} old stocks...")
        db.query(PriceHistory).delete()
        db.query(Stock).delete()
        db.commit()
        
        # Fetch ALL real stocks from NEPSE API
        print("Fetching ALL NEPSE stocks from API...")
        companies = NepseDataService.get_all_stocks()
        
        if not companies or len(companies) == 0:
            print("No stocks from API, using mock data instead...")
            # Use mock data as fallback
            for symbol, info in MockNEPSEDataProvider.STOCKS.items():
                current_price = MockNEPSEDataProvider.get_stock_price(symbol)
                stock = Stock(
                    symbol=symbol,
                    name=info["name"],
                    sector=info["sector"],
                    current_price=current_price,
                )
                db.add(stock)
            
            stocks_added = len(MockNEPSEDataProvider.STOCKS)
            data_source = "Mock Data (API unavailable)"
            
            db.commit()
            
            # Add mock historical data
            for symbol in MockNEPSEDataProvider.STOCKS.keys():
                historical_data = MockNEPSEDataProvider.get_historical_data(symbol, days=200)
                
                for data in historical_data:
                    price_history = PriceHistory(
                        stock_symbol=symbol,
                        date=data["date"],
                        open_price=data["open"],
                        high_price=data["high"],
                        low_price=data["low"],
                        close_price=data["close"],
                        volume=data["volume"],
                    )
                    db.add(price_history)
            
            db.commit()
        else:
            print(f"Successfully fetched {len(companies)} stocks from NEPSE API")
            data_source = "Real NEPSE API (nepseapi.surajrimal.dev)"
            
            # Also try to get price/volume data
            price_volume_data = NepseDataService.get_price_volume()
            print(f"Got price/volume for {len(price_volume_data)} stocks")
            
            stocks_added = 0
            
            # Add stocks from API
            for company in companies:
                try:
                    symbol = company.get('symbol', '').strip().upper()
                    if not symbol:
                        continue
                    
                    # Avoid duplicates
                    if db.query(Stock).filter_by(symbol=symbol).first():
                        continue
                    
                    # Get price data
                    pv_data = price_volume_data.get(symbol, {})
                    
                    stock = Stock(
                        symbol=symbol,
                        name=company.get('name', symbol),
                        sector=company.get('sector', 'Not Available'),
                        current_price=float(pv_data.get('ltp', company.get('ltp', 0)) or 0),
                    )
                    db.add(stock)
                    stocks_added += 1
                    
                except Exception as e:
                    logger.error(f"Error adding stock: {str(e)}")
                    continue
            
            db.commit()
            print(f"Added {stocks_added} stocks from API")
        
        # Add historical data for technical analysis (sample data for all stocks)
        print("Adding historical data for technical analysis...")
        for stock in db.query(Stock).all():
            try:
                historical_data = MockNEPSEDataProvider.get_historical_data(stock.symbol, days=200)
                
                for data in historical_data:
                    # Avoid duplicates
                    existing = db.query(PriceHistory).filter_by(
                        stock_symbol=stock.symbol,
                        date=data["date"]
                    ).first()
                    if existing:
                        continue
                    
                    price_history = PriceHistory(
                        stock_symbol=stock.symbol,
                        date=data["date"],
                        open_price=data["open"],
                        high_price=data["high"],
                        low_price=data["low"],
                        close_price=data["close"],
                        volume=data["volume"],
                    )
                    db.add(price_history)
            except Exception as e:
                print(f"Error adding history for {stock.symbol}: {str(e)}")
                continue
        
        db.commit()
        
        # Calculate technical analysis for all stocks
        print("Calculating technical analysis...")
        analysis_count = 0
        for stock in db.query(Stock).all():
            try:
                StockService.calculate_and_update_analysis(db, stock.symbol)
                analysis_count += 1
            except Exception as e:
                print(f"Error analyzing {stock.symbol}: {str(e)}")
                continue
        
        total_stocks = db.query(Stock).count()
        
        return {
            "message": "Database initialized successfully with ALL NEPSE stocks!",
            "total_stocks": total_stocks,
            "stocks_with_analysis": analysis_count,
            "data_source": "Real NEPSE API (nepseapi.surajrimal.dev)",
            "historical_data_days": 200,
            "update_time": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        print(f"Error in initialize: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=list[StockResponse])
def list_stocks(db: Session = Depends(get_db)):
    """Get all stocks with their current data"""
    stocks = db.query(Stock).all()
    return stocks


@router.get("/search")
def search_stocks(query: str, db: Session = Depends(get_db)):
    """Search stocks by symbol or name (uses mock data for demo)"""
    # For demo, we use mock data
    results = MockNEPSEDataProvider.search_stocks(query)
    return results


@router.get("/{symbol}", response_model=StockResponse)
def get_stock(symbol: str, db: Session = Depends(get_db)):
    """Get specific stock information"""
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    return stock


@router.put("/{symbol}", response_model=StockResponse)
def update_stock(
    symbol: str,
    stock_update: StockUpdate,
    db: Session = Depends(get_db)
):
    """Update stock information (admin endpoint)"""
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    # Update fields
    if stock_update.current_price is not None:
        stock.current_price = stock_update.current_price
    if stock_update.ma_50 is not None:
        stock.ma_50 = stock_update.ma_50
    if stock_update.ma_200 is not None:
        stock.ma_200 = stock_update.ma_200
    if stock_update.rsi is not None:
        stock.rsi = stock_update.rsi
    if stock_update.volume_trend is not None:
        stock.volume_trend = stock_update.volume_trend
    if stock_update.analysis_score is not None:
        stock.analysis_score = stock_update.analysis_score
    if stock_update.analysis_recommendation is not None:
        stock.analysis_recommendation = stock_update.analysis_recommendation
    
    stock.last_update = datetime.utcnow()
    db.commit()
    db.refresh(stock)
    
    return stock


@router.get("/{symbol}/history")
def get_price_history(
    symbol: str,
    days: int = 60,
    db: Session = Depends(get_db)
):
    """Get price history for a stock (for charts)"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    history = db.query(PriceHistory).filter(
        PriceHistory.stock_symbol == symbol.upper(),
        PriceHistory.date >= cutoff_date
    ).order_by(PriceHistory.date).all()
    
    if not history:
        raise HTTPException(status_code=404, detail=f"No price history found for {symbol}")
    
    return [{
        "date": h.date.isoformat(),
        "open": h.open_price,
        "high": h.high_price,
        "low": h.low_price,
        "close": h.close_price,
        "volume": h.volume,
    } for h in history]


@router.post("/update-prices")
def update_all_prices(db: Session = Depends(get_db)):
    """Update current prices for all stocks (called by scheduler)"""
    stocks = db.query(Stock).all()
    updated_count = 0
    
    for stock in stocks:
        # Get new price from mock data provider
        new_price = MockNEPSEDataProvider.get_stock_price(stock.symbol)
        StockService.update_stock_price(db, stock.symbol, new_price)
        StockService.calculate_and_update_analysis(db, stock.symbol)
        updated_count += 1
    
    return {"message": f"Updated prices for {updated_count} stocks"}


@router.get("/{symbol}/technical-analysis")
def get_technical_analysis(symbol: str, db: Session = Depends(get_db)):
    """Get technical analysis for a stock"""
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    return {
        "symbol": stock.symbol,
        "name": stock.name,
        "current_price": stock.current_price,
        "ma_50": stock.ma_50,
        "ma_200": stock.ma_200,
        "rsi": stock.rsi,
        "volume_trend": stock.volume_trend,
        "analysis_score": stock.analysis_score,
        "recommendation": stock.analysis_recommendation,
        "high_52w": stock.high_52w,
        "low_52w": stock.low_52w,
        "recent_high": stock.recent_high,
    }

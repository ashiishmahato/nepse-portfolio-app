"""
Background task scheduler for updating prices and generating alerts
Run this separately: python scheduler.py
"""
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services.stock_service import StockService, PortfolioService, AlertService
from app.models import Stock
from app.utils.mock_data import MockNEPSEDataProvider
from app.config import get_settings

settings = get_settings()


def update_stock_prices():
    """Update stock prices from API/mock data"""
    print(f"\n[{datetime.now()}] Updating stock prices...")
    
    db = SessionLocal()
    try:
        stocks = db.query(Stock).all()
        
        for stock in stocks:
            # Get new price from mock data provider
            new_price = MockNEPSEDataProvider.get_stock_price(stock.symbol)
            StockService.update_stock_price(db, stock.symbol, new_price)
            print(f"  {stock.symbol}: {new_price}")
        
        print(f"[{datetime.now()}] Prices updated for {len(stocks)} stocks")
    
    except Exception as e:
        print(f"Error updating prices: {e}")
    
    finally:
        db.close()


def calculate_technical_analysis():
    """Calculate technical analysis for all stocks"""
    print(f"\n[{datetime.now()}] Calculating technical analysis...")
    
    db = SessionLocal()
    try:
        stocks = db.query(Stock).all()
        
        for stock in stocks:
            StockService.calculate_and_update_analysis(db, stock.symbol)
            print(f"  {stock.symbol}: Analysis updated")
        
        print(f"[{datetime.now()}] Technical analysis updated")
    
    except Exception as e:
        print(f"Error calculating analysis: {e}")
    
    finally:
        db.close()


def update_portfolio_and_generate_alerts():
    """Update portfolio values and generate alerts"""
    print(f"\n[{datetime.now()}] Updating portfolio and generating alerts...")
    
    db = SessionLocal()
    try:
        # Update portfolio values
        PortfolioService.update_portfolio_values(db)
        
        # Generate new alerts
        AlertService.generate_alerts(db)
        
        # Deactivate expired alerts
        AlertService.deactivate_expired_alerts(db)
        
        print(f"[{datetime.now()}] Portfolio updated and alerts generated")
    
    except Exception as e:
        print(f"Error updating portfolio: {e}")
    
    finally:
        db.close()


def start_scheduler():
    """Start background scheduler"""
    scheduler = BackgroundScheduler()
    
    # Update prices every 5 minutes
    scheduler.add_job(
        update_stock_prices,
        'interval',
        minutes=1,  # Changed to 1 minute for demo purposes
        id='update_prices'
    )
    
    # Calculate technical analysis every 15 minutes
    scheduler.add_job(
        calculate_technical_analysis,
        'interval',
        minutes=5,  # Changed to 5 minutes for demo purposes
        id='calculate_analysis'
    )
    
    # Update portfolio and generate alerts every 10 minutes
    scheduler.add_job(
        update_portfolio_and_generate_alerts,
        'interval',
        minutes=2,  # Changed to 2 minutes for demo purposes
        id='update_portfolio'
    )
    
    scheduler.start()
    
    print("\n" + "="*50)
    print("Background Scheduler Started")
    print("="*50)
    print("Scheduled Jobs:")
    print("  - Update stock prices: Every 1 minute")
    print("  - Calculate technical analysis: Every 5 minutes")
    print("  - Update portfolio and alerts: Every 2 minutes")
    print("="*50 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped")
        scheduler.shutdown()


if __name__ == "__main__":
    start_scheduler()

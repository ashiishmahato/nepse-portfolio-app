"""
API routes for portfolio management
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PortfolioCreate, PortfolioUpdate, PortfolioResponse, DashboardSummary
from app.models import Portfolio, Stock
from app.services.stock_service import PortfolioService, StockService, AlertService
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.post("/add", response_model=PortfolioResponse)
def add_to_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db)
):
    """
    Add a stock to user's portfolio
    
    - **stock_symbol**: Stock symbol (e.g., NABIL)
    - **buy_price**: Price at which stock was bought
    - **quantity**: Number of shares
    - **target_profit_percentage**: Target profit % (e.g., 15)
    - **stop_loss_percentage**: Optional stop loss %
    - **purchase_date**: Optional purchase date (e.g., 2024-08-05)
    """
    # Verify stock exists
    stock = db.query(Stock).filter(Stock.symbol == portfolio.stock_symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {portfolio.stock_symbol} not found")
    
    # Create portfolio entry
    total_invested = portfolio.buy_price * portfolio.quantity
    
    # Convert 0 stop loss to None (no stop loss)
    stop_loss = portfolio.stop_loss_percentage if portfolio.stop_loss_percentage and portfolio.stop_loss_percentage > 0 else None
    
    db_portfolio = Portfolio(
        stock_symbol=portfolio.stock_symbol,
        buy_price=portfolio.buy_price,
        quantity=portfolio.quantity,
        target_profit_percentage=portfolio.target_profit_percentage,
        stop_loss_percentage=stop_loss,
        total_invested=total_invested,
        current_value=stock.current_price * portfolio.quantity,
        purchase_date=portfolio.purchase_date or datetime.utcnow(),
        notes=portfolio.notes,
    )
    
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    
    # Generate alerts for this new entry
    AlertService.generate_alerts(db)
    
    return db_portfolio


@router.get("/list", response_model=list[PortfolioResponse])
def get_portfolio(
    include_sold: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all portfolio holdings
    
    - **include_sold**: Include sold positions (default: False)
    """
    if include_sold:
        items = db.query(Portfolio).all()
    else:
        items = db.query(Portfolio).filter(Portfolio.is_sold == 0).all()
    
    return items


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio_item(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get specific portfolio item"""
    item = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    return item


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,
    db: Session = Depends(get_db)
):
    """Update portfolio entry"""
    item = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    if portfolio_update.target_profit_percentage is not None:
        item.target_profit_percentage = portfolio_update.target_profit_percentage
    
    if portfolio_update.stop_loss_percentage is not None:
        # Convert 0 to None (no stop loss)
        item.stop_loss_percentage = portfolio_update.stop_loss_percentage if portfolio_update.stop_loss_percentage > 0 else None
    
    if portfolio_update.purchase_date is not None:
        item.purchase_date = portfolio_update.purchase_date
    
    if portfolio_update.notes is not None:
        item.notes = portfolio_update.notes
    
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    
    return item


@router.delete("/{portfolio_id}")
def remove_from_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Remove stock from portfolio (mark as sold)"""
    item = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    item.is_sold = 1
    item.sell_date = datetime.utcnow()
    
    # Get current stock price as sell price
    stock = db.query(Stock).filter(Stock.symbol == item.stock_symbol).first()
    if stock:
        item.sell_price = stock.current_price
    
    db.commit()
    
    return {"message": "Item removed from portfolio", "portfolio_id": portfolio_id}


@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard summary with portfolio and alert information"""
    try:
        # Update portfolio values
        PortfolioService.update_portfolio_values(db)
        
        # Get summary
        summary = PortfolioService.get_dashboard_summary(db)
        
        # Get portfolio items
        portfolio_items = db.query(Portfolio).filter(Portfolio.is_sold == 0).all()
        
        # Get recent alerts
        from app.models import Alert
        recent_alerts = db.query(Alert).filter(Alert.is_active == 1).order_by(Alert.created_at.desc()).limit(10).all()
        
        # Convert to dictionaries for proper serialization
        summary["portfolio_items"] = [
            {
                "id": item.id,
                "stock_symbol": item.stock_symbol,
                "quantity": item.quantity,
                "buy_price": item.buy_price,
                "total_invested": item.total_invested,
                "current_value": item.current_value,
                "profit_loss": item.profit_loss,
                "profit_loss_percentage": item.profit_loss_percentage,
            }
            for item in portfolio_items
        ]
        
        summary["recent_alerts"] = [
            {
                "id": alert.id,
                "stock_symbol": alert.stock_symbol,
                "alert_type": alert.alert_type,
                "trigger_price": alert.trigger_price,
                "is_active": alert.is_active,
                "created_at": alert.created_at.isoformat() if alert.created_at else None,
            }
            for alert in recent_alerts
        ]
        
        return summary
    except Exception as e:
        logger.error(f"Error fetching dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

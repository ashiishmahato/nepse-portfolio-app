"""
Portfolio model for storing user's stock holdings
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, func
from datetime import datetime
from app.database import Base


class Portfolio(Base):
    """User portfolio model"""
    __tablename__ = "portfolio"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, index=True)  # Reference to stock symbol (NABIL, etc.)
    buy_price = Column(Float)  # Price at which user bought
    quantity = Column(Integer)  # Number of shares
    target_profit_percentage = Column(Float)  # Target profit % (e.g., 15)
    stop_loss_percentage = Column(Float, nullable=True)  # Stop loss % (e.g., 10)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Calculated fields
    total_invested = Column(Float)  # buy_price * quantity
    current_value = Column(Float, default=0.0)  # current_price * quantity
    profit_loss = Column(Float, default=0.0)  # current_value - total_invested
    profit_loss_percentage = Column(Float, default=0.0)
    
    # Status tracking
    is_sold = Column(Integer, default=0)  # 0 = holding, 1 = sold
    sell_price = Column(Float, nullable=True)
    sell_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Portfolio(symbol={self.stock_symbol}, qty={self.quantity}, buy_price={self.buy_price})>"

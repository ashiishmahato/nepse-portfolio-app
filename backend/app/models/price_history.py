"""
Price history model for storing historical stock prices
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, func
from datetime import datetime
from app.database import Base


class PriceHistory(Base):
    """Historical price data for technical analysis"""
    __tablename__ = "price_history"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, index=True)
    date = Column(DateTime, index=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    
    def __repr__(self):
        return f"<PriceHistory(symbol={self.stock_symbol}, date={self.date}, close={self.close_price})>"
